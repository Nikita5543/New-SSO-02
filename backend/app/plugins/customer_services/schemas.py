from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CustomerServiceBase(BaseModel):
    base_id: Optional[str] = None
    activity: Optional[str] = None
    client: Optional[str] = None
    contract: Optional[str] = None
    type_of_service: Optional[str] = None
    status: Optional[str] = None
    order_num: Optional[str] = None
    first_point: Optional[str] = None
    second_point: Optional[str] = None
    speed: Optional[str] = None
    vlan_id: Optional[str] = None
    switchboard_first_point: Optional[str] = None
    switch_port_first_point: Optional[str] = None
    port_settings_first_point: Optional[str] = None
    switchboard_second_point: Optional[str] = None
    switch_port_second_point: Optional[str] = None
    port_settings_second_point: Optional[str] = None
    subnets: Optional[str] = None
    router: Optional[str] = None
    interface: Optional[str] = None
    auto_network: Optional[str] = None
    end_client: Optional[str] = None
    last_mile: Optional[str] = None
    id_servicepipe: Optional[str] = None
    comment: Optional[str] = None
    responsible_department: Optional[str] = None


class CustomerServiceCreate(CustomerServiceBase):
    pass


class CustomerServiceUpdate(CustomerServiceBase):
    pass


class CustomerServiceResponse(CustomerServiceBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CustomerServiceListResponse(BaseModel):
    count: int
    results: list[CustomerServiceResponse]
