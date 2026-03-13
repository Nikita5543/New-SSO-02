from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.plugins.performance.models import MonitorTarget, MetricSample
from app.plugins.performance.schemas import MonitorTargetCreate, MonitorTargetResponse, MetricSampleResponse

router = APIRouter()


@router.get("/targets", response_model=List[MonitorTargetResponse])
def list_targets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return db.query(MonitorTarget).all()


@router.post("/targets", response_model=MonitorTargetResponse)
def create_target(
    data: MonitorTargetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    target = MonitorTarget(**data.model_dump())
    db.add(target)
    db.commit()
    db.refresh(target)
    return target


@router.get("/targets/{target_id}", response_model=MonitorTargetResponse)
def get_target(
    target_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    target = db.query(MonitorTarget).filter(MonitorTarget.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Monitor target not found")
    return target


@router.delete("/targets/{target_id}")
def delete_target(
    target_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    target = db.query(MonitorTarget).filter(MonitorTarget.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Monitor target not found")
    db.delete(target)
    db.commit()
    return {"status": "ok", "message": "Target deleted"}


@router.get("/metrics/{target_id}", response_model=List[MetricSampleResponse])
def get_metrics(
    target_id: int,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return (
        db.query(MetricSample)
        .filter(MetricSample.target_id == target_id)
        .order_by(MetricSample.collected_at.desc())
        .limit(limit)
        .all()
    )
