from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class MonitorTarget(Base):
    __tablename__ = "monitor_targets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    target_type = Column(String(50), nullable=False)  # host, interface, service
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=True)
    protocol = Column(String(20), nullable=True)
    interval_seconds = Column(Integer, default=60)
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MetricSample(Base):
    __tablename__ = "metric_samples"

    id = Column(Integer, primary_key=True, index=True)
    target_id = Column(Integer, ForeignKey("monitor_targets.id"), nullable=False)
    metric_name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=True)
    collected_at = Column(DateTime(timezone=True), server_default=func.now())
