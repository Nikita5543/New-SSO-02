from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ConfigSnapshotCreate(BaseModel):
    device_name: str
    config_type: str = "running"
    content: str
    version: Optional[str] = None
    collected_by: Optional[str] = None


class ConfigSnapshotResponse(BaseModel):
    id: int
    device_name: str
    config_type: str
    content: str
    version: Optional[str] = None
    collected_by: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ConfigTemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    template_content: str
    vendor: Optional[str] = None


class ConfigTemplateResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    template_content: str
    vendor: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
