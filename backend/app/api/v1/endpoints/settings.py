from fastapi import APIRouter, Depends
from app.core.security import get_current_admin_user
from app.models.user import User

router = APIRouter()


@router.get("/")
async def get_settings(
    current_user: User = Depends(get_current_admin_user),
):
    return {
        "app_name": "NOC Vision",
        "version": "1.0.0",
        "theme": "dark",
        "language": "ru",
    }
