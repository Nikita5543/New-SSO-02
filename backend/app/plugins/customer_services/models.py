from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class CustomerService(Base):
    """Модель для хранения услуг клиентов"""
    __tablename__ = "customer_services"

    id = Column(Integer, primary_key=True, index=True)
    base_id = Column(String(50), index=True)
    activity = Column(String(100))
    client = Column(String(255))
    contract = Column(String(255))
    type_of_service = Column(String(255))
    status = Column(String(50), index=True)
    order_num = Column(String(100))
    first_point = Column(Text)
    second_point = Column(Text)
    speed = Column(String(100))
    vlan_id = Column(String(100))
    switchboard_first_point = Column(String(255))
    switch_port_first_point = Column(String(255))
    port_settings_first_point = Column(Text)
    switchboard_second_point = Column(String(255))
    switch_port_second_point = Column(String(255))
    port_settings_second_point = Column(Text)
    subnets = Column(String(255))
    router = Column(String(255))
    interface = Column(String(255))
    auto_network = Column(String(100))
    end_client = Column(String(255))
    last_mile = Column(String(255))
    id_servicepipe = Column(String(100))
    comment = Column(Text)
    responsible_department = Column(String(100))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "base_id": self.base_id,
            "activity": self.activity,
            "client": self.client,
            "contract": self.contract,
            "type_of_service": self.type_of_service,
            "status": self.status,
            "order_num": self.order_num,
            "first_point": self.first_point,
            "second_point": self.second_point,
            "speed": self.speed,
            "vlan_id": self.vlan_id,
            "switchboard_first_point": self.switchboard_first_point,
            "switch_port_first_point": self.switch_port_first_point,
            "port_settings_first_point": self.port_settings_first_point,
            "switchboard_second_point": self.switchboard_second_point,
            "switch_port_second_point": self.switch_port_second_point,
            "port_settings_second_point": self.port_settings_second_point,
            "subnets": self.subnets,
            "router": self.router,
            "interface": self.interface,
            "auto_network": self.auto_network,
            "end_client": self.end_client,
            "last_mile": self.last_mile,
            "id_servicepipe": self.id_servicepipe,
            "comment": self.comment,
            "responsible_department": self.responsible_department,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
