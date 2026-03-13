from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.plugins.configuration.models import ConfigSnapshot, ConfigTemplate
from app.plugins.configuration.schemas import (
    ConfigSnapshotCreate, ConfigSnapshotResponse,
    ConfigTemplateCreate, ConfigTemplateResponse,
)

router = APIRouter()


@router.get("/snapshots", response_model=List[ConfigSnapshotResponse])
def list_snapshots(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return db.query(ConfigSnapshot).offset(skip).limit(limit).all()


@router.post("/snapshots", response_model=ConfigSnapshotResponse)
def create_snapshot(
    data: ConfigSnapshotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    snapshot = ConfigSnapshot(**data.model_dump())
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot


@router.get("/snapshots/{snapshot_id}", response_model=ConfigSnapshotResponse)
def get_snapshot(
    snapshot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    snapshot = db.query(ConfigSnapshot).filter(ConfigSnapshot.id == snapshot_id).first()
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return snapshot


@router.get("/templates", response_model=List[ConfigTemplateResponse])
def list_templates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return db.query(ConfigTemplate).all()


@router.post("/templates", response_model=ConfigTemplateResponse)
def create_template(
    data: ConfigTemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    template = ConfigTemplate(**data.model_dump())
    db.add(template)
    db.commit()
    db.refresh(template)
    return template
