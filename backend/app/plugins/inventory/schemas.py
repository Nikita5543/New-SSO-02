from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DeviceCreate(BaseModel):
    name: str
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    site_id: Optional[int] = None
    device_type_id: Optional[int] = None
    serial_number: Optional[str] = None
    status: str = "active"
    notes: Optional[str] = None


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    site_id: Optional[int] = None
    device_type_id: Optional[int] = None
    serial_number: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class DeviceResponse(BaseModel):
    id: int
    name: str
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    site_id: Optional[int] = None
    device_type_id: Optional[int] = None
    serial_number: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class SiteCreate(BaseModel):
    name: str
    address: Optional[str] = None
    description: Optional[str] = None


class SiteResponse(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class DeviceTypeCreate(BaseModel):
    name: str
    manufacturer: Optional[str] = None
    model: Optional[str] = None


class DeviceTypeResponse(BaseModel):
    id: int
    name: str
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
