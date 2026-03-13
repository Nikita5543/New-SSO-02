from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class IncidentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    severity: str = "minor"
    assigned_to: Optional[int] = None
    affected_system: Optional[str] = None


class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[int] = None
    affected_system: Optional[str] = None


class IncidentResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    severity: str
    status: str
    assigned_to: Optional[int] = None
    affected_system: Optional[str] = None
    created_by: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class IncidentCommentCreate(BaseModel):
    text: str


class IncidentCommentResponse(BaseModel):
    id: int
    incident_id: int
    user_id: int
    text: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
