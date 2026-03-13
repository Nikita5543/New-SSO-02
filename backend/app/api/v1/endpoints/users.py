from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.common import StatusResponse
from app.services import user_service

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    return user_service.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Non-admin can only view their own profile
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user


@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    if user_service.get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if user_service.get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(
        db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name,
        role=user_data.role,
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_service.update_user(db, user, **user_data.model_dump(exclude_unset=True))


@router.delete("/{user_id}", response_model=StatusResponse)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_service.delete_user(db, user)
    return {"status": "ok", "message": "User deleted"}
