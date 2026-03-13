from sqlalchemy import Column, Integer, String, DateTime, Float, BigInteger, Text
from sqlalchemy.sql import func
from app.core.database import Base


class Interface(Base):
    __tablename__ = "interfaces"

    id = Column(Integer, primary_key=True, index=True)
    device_name = Column(String(100), nullable=False)
    interface_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    speed_mbps = Column(Integer, nullable=True)
    status = Column(String(20), default="up")  # up, down, admin_down
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TrafficRecord(Base):
    __tablename__ = "traffic_records"

    id = Column(Integer, primary_key=True, index=True)
    interface_id = Column(Integer, nullable=False)
    bytes_in = Column(BigInteger, default=0)
    bytes_out = Column(BigInteger, default=0)
    packets_in = Column(BigInteger, default=0)
    packets_out = Column(BigInteger, default=0)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
