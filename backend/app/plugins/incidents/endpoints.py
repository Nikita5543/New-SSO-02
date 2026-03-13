from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.plugins.incidents.models import Incident, IncidentComment
from app.plugins.incidents.schemas import (
    IncidentCreate, IncidentUpdate, IncidentResponse,
    IncidentCommentCreate, IncidentCommentResponse,
)

router = APIRouter()


@router.get("/", response_model=List[IncidentResponse])
def list_incidents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return db.query(Incident).order_by(Incident.created_at.desc()).offset(skip).limit(limit).all()


@router.post("/", response_model=IncidentResponse)
def create_incident(
    data: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    incident = Incident(**data.model_dump(), created_by=current_user.id)
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int,
    data: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    update_data = data.model_dump(exclude_unset=True)
    if update_data.get("status") == "resolved" and incident.status != "resolved":
        update_data["resolved_at"] = datetime.now(timezone.utc)
    for key, value in update_data.items():
        setattr(incident, key, value)
    db.commit()
    db.refresh(incident)
    return incident


@router.delete("/{incident_id}")
def delete_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    db.delete(incident)
    db.commit()
    return {"status": "ok", "message": "Incident deleted"}


# --- Comments ---

@router.get("/{incident_id}/comments", response_model=List[IncidentCommentResponse])
def list_comments(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return (
        db.query(IncidentComment)
        .filter(IncidentComment.incident_id == incident_id)
        .order_by(IncidentComment.created_at.asc())
        .all()
    )


@router.post("/{incident_id}/comments", response_model=IncidentCommentResponse)
def add_comment(
    incident_id: int,
    data: IncidentCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    comment = IncidentComment(
        incident_id=incident_id,
        user_id=current_user.id,
        text=data.text,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
