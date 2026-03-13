from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class ConfigSnapshot(Base):
    __tablename__ = "config_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    device_name = Column(String(100), nullable=False)
    config_type = Column(String(50), default="running")  # running, startup
    content = Column(Text, nullable=False)
    version = Column(String(50), nullable=True)
    collected_by = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ConfigTemplate(Base):
    __tablename__ = "config_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    template_content = Column(Text, nullable=False)
    vendor = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
