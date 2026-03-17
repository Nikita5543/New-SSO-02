from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.schemas.auth import (
    TokenPairWithUser,
    RefreshRequest,
    LogoutRequest,
)
from app.schemas.user import UserCreate, UserResponse
from app.schemas.common import StatusResponse
from app.services import auth_service

router = APIRouter()


@router.post("/login", response_model=TokenPairWithUser)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = auth_service.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )
    return auth_service.create_token_pair(user, db)


@router.post("/refresh", response_model=TokenPairWithUser)
async def refresh_token(
    request: RefreshRequest,
    db: Session = Depends(get_db),
):
    result = auth_service.refresh_access_token(request.refresh_token, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    return result


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    from app.services import user_service

    if user_service.get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    if user_service.get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = user_service.create_user(
        db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name,
        role=user_data.role,
    )
    return user


@router.post("/logout", response_model=StatusResponse)
async def logout(
    request: LogoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    auth_service.revoke_token(request.refresh_token, db)
    return {"status": "ok", "message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
):
    return current_user


@router.post("/init", response_model=StatusResponse)
async def init_admin(db: Session = Depends(get_db)):
    admin = auth_service.create_default_admin(db)
    if admin:
        return {"status": "ok", "message": f"Admin user '{admin.username}' created"}
    return {"status": "ok", "message": "Admin user already exists"}
