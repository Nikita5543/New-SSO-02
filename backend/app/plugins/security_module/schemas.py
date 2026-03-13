from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    action: str
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    details: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class SecurityEventCreate(BaseModel):
    event_type: str
    severity: str = "info"
    source_ip: Optional[str] = None
    description: Optional[str] = None


class SecurityEventResponse(BaseModel):
    id: int
    event_type: str
    severity: str
    source_ip: Optional[str] = None
    description: Optional[str] = None
    resolved: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
