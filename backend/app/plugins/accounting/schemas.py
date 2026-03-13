from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InterfaceCreate(BaseModel):
    device_name: str
    interface_name: str
    description: Optional[str] = None
    speed_mbps: Optional[int] = None
    status: str = "up"


class InterfaceResponse(BaseModel):
    id: int
    device_name: str
    interface_name: str
    description: Optional[str] = None
    speed_mbps: Optional[int] = None
    status: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class TrafficRecordResponse(BaseModel):
    id: int
    interface_id: int
    bytes_in: int
    bytes_out: int
    packets_in: int
    packets_out: int
    recorded_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
