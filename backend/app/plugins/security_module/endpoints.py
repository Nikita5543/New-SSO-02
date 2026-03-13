from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.plugins.security_module.models import AuditLog, SecurityEvent
from app.plugins.security_module.schemas import (
    AuditLogResponse,
    SecurityEventCreate, SecurityEventResponse,
)

router = APIRouter()


@router.get("/audit-logs", response_model=List[AuditLogResponse])
def list_audit_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    return (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/events", response_model=List[SecurityEventResponse])
def list_security_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return (
        db.query(SecurityEvent)
        .order_by(SecurityEvent.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.post("/events", response_model=SecurityEventResponse)
def create_security_event(
    data: SecurityEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    event = SecurityEvent(**data.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("/events/{event_id}", response_model=SecurityEventResponse)
def get_security_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    event = db.query(SecurityEvent).filter(SecurityEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Security event not found")
    return event
