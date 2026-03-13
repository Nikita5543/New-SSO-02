from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.services import user_service

router = APIRouter()


@router.get("/")
async def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    total_users = user_service.get_user_count(db)
    loaded_plugins = getattr(current_user, "_app_plugins", [])

    return {
        "welcome": f"Welcome, {current_user.full_name or current_user.username}!",
        "stats": {
            "total_users": total_users,
            "your_role": current_user.role,
        },
    }
