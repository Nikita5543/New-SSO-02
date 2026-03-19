from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class NetworkDevice(Base):
    """Network devices from NetBox"""
    __tablename__ = "network_devices"
    
    id = Column(Integer, primary_key=True, index=True)
    netbox_id = Column(Integer, unique=True, index=True)
    hostname = Column(String(100), nullable=False)
    mgmt_ip = Column(String(50), nullable=False)
    platform = Column(String(100))
    device_role = Column(String(50))
    site = Column(String(100))
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "netbox_id": self.netbox_id,
            "hostname": self.hostname,
            "mgmt_ip": self.mgmt_ip,
            "platform": self.platform,
            "device_role": self.device_role,
            "site": self.site,
            "status": self.status,
        }


class DeviceCheckResult(Base):
    """Results of device status checks"""
    __tablename__ = "device_check_results"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("network_devices.id"), nullable=False)
    check_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Status fields from screenshot
    operational_status = Column(String(20))  # Online/Offline
    backup_status = Column(String(20))       # OK/Failed/NONE
    snapshot_status = Column(String(20))     # OK/Failed/NONE
    critical_alarm = Column(String(10))      # YES/NO
    
    # Raw output from script
    raw_output = Column(Text)
    check_status = Column(String(20), default="pending")  # pending/running/completed/failed
    error_message = Column(Text)
    
    def to_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "check_date": self.check_date.isoformat() if self.check_date else None,
            "operational_status": self.operational_status,
            "backup_status": self.backup_status,
            "snapshot_status": self.snapshot_status,
            "critical_alarm": self.critical_alarm,
            "check_status": self.check_status,
            "error_message": self.error_message,
        }
