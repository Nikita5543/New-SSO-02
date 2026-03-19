from typing import List
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_superuser, check_plugin_access
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.common import StatusResponse
from app.services import user_service

router = APIRouter()


@router.get("/me/permissions")
async def get_user_permissions(
    current_user: User = Depends(get_current_active_user),
):
    """Получить права доступа текущего пользователя"""
    return {
        "role": current_user.role,
        "can_access_admin": current_user.role == "superuser",
        "sections": ["operations"] if current_user.role == "user" else ["operations", "analytics", "security", "admin"]
    }


@router.put("/me/avatar", response_model=UserResponse)
async def update_my_avatar(
    avatar_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Обновить аватар текущего пользователя"""
    avatar_url = avatar_data.get("avatar_url")
    return user_service.update_user(db, current_user, avatar_url=avatar_url)


@router.put("/me/background", response_model=UserResponse)
async def update_my_background(
    background_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Обновить фон текущего пользователя"""
    background_image = background_data.get("background_image")
    return user_service.update_user(db, current_user, background_image=background_image)


@router.get("/me/backgrounds-list")
async def get_backgrounds_list(
    current_user: User = Depends(get_current_active_user),
):
    """Получить список доступных фонов"""
    ALLOWED_EXT = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'}
    # In Docker, frontend static files are served by nginx.
    # We look in /usr/share/nginx/html/backgrounds (nginx static dir)
    # or fallback to a hardcoded list based on known filenames.
    import os
    nginx_path = Path('/usr/share/nginx/html/backgrounds')
    local_path = Path(__file__).resolve().parents[4] / 'frontend' / 'public' / 'backgrounds'
    
    for search_dir in [nginx_path, local_path]:
        if search_dir.exists():
            files = [
                f.name for f in sorted(search_dir.iterdir())
                if f.is_file() and f.suffix.lower() in ALLOWED_EXT
            ]
            return {"backgrounds": files}
    
    return {"backgrounds": []}


@router.get("/plugins/access/{section}")
async def check_plugin_section_access(
    section: str,
    current_user: User = Depends(get_current_active_user),
):
    """Проверить доступ к секции плагинов"""
    has_access = check_plugin_access(current_user.role, section)
    return {
        "section": section,
        "has_access": has_access,
        "role": current_user.role
    }


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    """Получить список всех пользователей (только superuser)"""
    return user_service.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Получить информацию о пользователе"""
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Non-superuser can only view their own profile
    if current_user.role != "superuser" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user


@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    """Создать нового пользователя (только superuser)"""
    if user_service.get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if user_service.get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Обычные пользователи не могут создавать superuser
    if user_data.role == "superuser" and current_user.role != "superuser":
        raise HTTPException(status_code=403, detail="Cannot create superuser")
    
    return user_service.create_user(
        db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name,
        role=user_data.role or "user",
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    """Обновить данные пользователя (только superuser)"""
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Проверка: нельзя изменить роль на superuser если ты не superuser
    if user_data.role == "superuser" and current_user.role != "superuser":
        raise HTTPException(status_code=403, detail="Cannot assign superuser role")
    
    # Нельзя деактивировать последнего superuser
    if user_data.is_active is False and user.role == "superuser":
        superusers_count = db.query(User).filter(User.role == "superuser", User.is_active == True).count()
        if superusers_count <= 1 and user.id == current_user.id:
            raise HTTPException(status_code=400, detail="Cannot deactivate the last superuser")
    
    return user_service.update_user(db, user, **user_data.model_dump(exclude_unset=True))


@router.delete("/{user_id}", response_model=StatusResponse)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    """Удалить пользователя (только superuser)"""
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Нельзя удалить последнего superuser
    if user.role == "superuser":
        superusers_count = db.query(User).filter(User.role == "superuser", User.is_active == True).count()
        if superusers_count <= 1:
            raise HTTPException(status_code=400, detail="Cannot delete the last superuser")
    
    user_service.delete_user(db, user)
    return {"status": "ok", "message": "User deleted"}
