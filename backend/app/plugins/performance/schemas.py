from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MonitorTargetCreate(BaseModel):
    name: str
    target_type: str = "host"
    host: str
    port: Optional[int] = None
    protocol: Optional[str] = None
    interval_seconds: int = 60


class MonitorTargetResponse(BaseModel):
    id: int
    name: str
    target_type: str
    host: str
    port: Optional[int] = None
    protocol: Optional[str] = None
    interval_seconds: int
    status: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class MetricSampleResponse(BaseModel):
    id: int
    target_id: int
    metric_name: str
    value: float
    unit: Optional[str] = None
    collected_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
