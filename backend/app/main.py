import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.core.plugin_loader import load_plugins
from app.api.v1.router import api_router
from app.models import User, RefreshToken  # noqa: ensure models are loaded
from app.services.auth_service import create_default_admin, cleanup_expired_tokens

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL, logging.INFO))

    # Create tables (fallback for dev; Alembic is preferred for production)
    Base.metadata.create_all(bind=engine)

    # Load plugins
    loaded_plugins = load_plugins(app)
    app.state.loaded_plugins = loaded_plugins

    # Re-create tables for any new plugin models
    Base.metadata.create_all(bind=engine)

    # Create default admin if none exists
    db = SessionLocal()
    try:
        admin = create_default_admin(db)
        if admin:
            logger.info(f"Default admin '{admin.username}' created")
        cleanup_expired_tokens(db)
    finally:
        db.close()

    logger.info(
        f"NOC Vision started. {len([p for p in loaded_plugins if p['status'] == 'loaded'])} plugins loaded."
    )
    yield
    # Shutdown
    engine.dispose()


app = FastAPI(
    title="NOC Vision API",
    description="Network Operations Center Platform API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "NOC Vision API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/api/v1/plugins")
async def list_plugins():
    return getattr(app.state, "loaded_plugins", [])
