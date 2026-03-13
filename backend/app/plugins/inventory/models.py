from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.core.database import Base


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    address = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DeviceType(Base):
    __tablename__ = "device_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    manufacturer = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    hostname = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=True)
    device_type_id = Column(Integer, ForeignKey("device_types.id"), nullable=True)
    serial_number = Column(String(100), nullable=True)
    status = Column(String(20), default="active")  # active, inactive, maintenance
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
