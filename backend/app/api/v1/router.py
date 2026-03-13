from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, dashboard, settings

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(settings.router, prefix="/settings", tags=["Settings"])
