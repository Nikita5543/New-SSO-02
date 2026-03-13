from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.plugins.inventory.models import Device, Site, DeviceType
from app.plugins.inventory.schemas import (
    DeviceCreate, DeviceUpdate, DeviceResponse,
    SiteCreate, SiteResponse,
    DeviceTypeCreate, DeviceTypeResponse,
)

router = APIRouter()


# --- Devices ---

@router.get("/devices", response_model=List[DeviceResponse])
def list_devices(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return db.query(Device).offset(skip).limit(limit).all()


@router.post("/devices", response_model=DeviceResponse)
def create_device(
    data: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    device = Device(**data.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


@router.get("/devices/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.put("/devices/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: int,
    data: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(device, key, value)
    db.commit()
    db.refresh(device)
    return device


@router.delete("/devices/{device_id}")
def delete_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(device)
    db.commit()
    return {"status": "ok", "message": "Device deleted"}


# --- Sites ---

@router.get("/sites", response_model=List[SiteResponse])
def list_sites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return db.query(Site).all()


@router.post("/sites", response_model=SiteResponse)
def create_site(
    data: SiteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    site = Site(**data.model_dump())
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


# --- Device Types ---

@router.get("/device-types", response_model=List[DeviceTypeResponse])
def list_device_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return db.query(DeviceType).all()


@router.post("/device-types", response_model=DeviceTypeResponse)
def create_device_type(
    data: DeviceTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    dt = DeviceType(**data.model_dump())
    db.add(dt)
    db.commit()
    db.refresh(dt)
    return dt
