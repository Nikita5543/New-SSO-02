from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=True)
    resource_id = Column(String(50), nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), nullable=False)  # login_failed, access_denied, suspicious_activity
    severity = Column(String(20), default="info")  # critical, high, medium, low, info
    source_ip = Column(String(45), nullable=True)
    description = Column(Text, nullable=True)
    resolved = Column(String(10), default="no")  # yes, no
    created_at = Column(DateTime(timezone=True), server_default=func.now())
