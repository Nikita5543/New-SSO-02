from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.plugins.accounting.models import Interface, TrafficRecord
from app.plugins.accounting.schemas import InterfaceCreate, InterfaceResponse, TrafficRecordResponse

router = APIRouter()


@router.get("/interfaces", response_model=List[InterfaceResponse])
def list_interfaces(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return db.query(Interface).all()


@router.post("/interfaces", response_model=InterfaceResponse)
def create_interface(
    data: InterfaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    iface = Interface(**data.model_dump())
    db.add(iface)
    db.commit()
    db.refresh(iface)
    return iface


@router.get("/interfaces/{interface_id}", response_model=InterfaceResponse)
def get_interface(
    interface_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    iface = db.query(Interface).filter(Interface.id == interface_id).first()
    if not iface:
        raise HTTPException(status_code=404, detail="Interface not found")
    return iface


@router.get("/traffic/{interface_id}", response_model=List[TrafficRecordResponse])
def get_traffic(
    interface_id: int,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return (
        db.query(TrafficRecord)
        .filter(TrafficRecord.interface_id == interface_id)
        .order_by(TrafficRecord.recorded_at.desc())
        .limit(limit)
        .all()
    )
