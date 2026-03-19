from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class NetworkDeviceBase(BaseModel):
    hostname: str
    mgmt_ip: str
    platform: Optional[str] = None
    device_role: Optional[str] = None
    site: Optional[str] = None
    status: Optional[str] = "active"


class NetworkDeviceCreate(NetworkDeviceBase):
    netbox_id: int


class NetworkDeviceResponse(NetworkDeviceBase):
    id: int
    netbox_id: int
    
    model_config = {"from_attributes": True}


class DeviceCheckResultBase(BaseModel):
    operational_status: Optional[str] = None
    backup_status: Optional[str] = None
    snapshot_status: Optional[str] = None
    critical_alarm: Optional[str] = None
    check_status: Optional[str] = "pending"
    error_message: Optional[str] = None


class DeviceCheckResultCreate(DeviceCheckResultBase):
    device_id: int


class DeviceCheckResultResponse(DeviceCheckResultBase):
    id: int
    device_id: int
    check_date: Optional[datetime] = None
    
    model_config = {"from_attributes": True}


class DeviceWithLatestCheck(BaseModel):
    """Device with its latest check result"""
    device: NetworkDeviceResponse
    latest_check: Optional[DeviceCheckResultResponse] = None


class DeviceStatusListResponse(BaseModel):
    devices: List[DeviceWithLatestCheck]
    total: int
    summary: dict


class CheckRunResponse(BaseModel):
    """Response when starting a check"""
    check_id: int
    device_id: int
    status: str
    message: str
