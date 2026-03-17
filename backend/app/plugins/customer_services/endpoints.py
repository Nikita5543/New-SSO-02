import csv
import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.plugins.customer_services.models import CustomerService
from app.plugins.customer_services.schemas import (
    CustomerServiceUpdate,
    CustomerServiceResponse,
    CustomerServiceListResponse,
)

router = APIRouter()

# Path to CSV file
CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "services.csv")


def load_csv_to_db(db: Session):
    """Load data from CSV file to database"""
    if not os.path.exists(CSV_PATH):
        return
    
    # Check if data already exists
    count = db.query(CustomerService).count()
    if count > 0:
        return  # Data already loaded
    
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            service = CustomerService(
                base_id=row.get('base_id'),
                activity=row.get('activity'),
                client=row.get('client'),
                contract=row.get('contract'),
                type_of_service=row.get('type_of_service'),
                status=row.get('status'),
                order_num=row.get('order_num'),
                first_point=row.get('first_point'),
                second_point=row.get('second_point'),
                speed=row.get('speed'),
                vlan_id=row.get('vlan_id'),
                switchboard_first_point=row.get('switchboard_first_point'),
                switch_port_first_point=row.get('switch_port_first_point'),
                port_settings_first_point=row.get('port_settings_first_point'),
                switchboard_second_point=row.get('switchboard_second_point'),
                switch_port_second_point=row.get('switch_port_second_point'),
                port_settings_second_point=row.get('port_settings_second_point'),
                subnets=row.get('subnets'),
                router=row.get('router'),
                interface=row.get('interface'),
                auto_network=row.get('auto_network'),
                end_client=row.get('end_client'),
                last_mile=row.get('last_mile'),
                id_servicepipe=row.get('id_servicepipe'),
                comment=row.get('comment'),
                responsible_department=row.get('responsible_department'),
            )
            db.add(service)
        db.commit()


@router.get("/services", response_model=CustomerServiceListResponse)
async def list_services(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    client: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get list of customer services with pagination and filtering"""
    # Load CSV data if not already loaded
    load_csv_to_db(db)
    
    query = db.query(CustomerService)
    
    # Apply filters - search across all columns
    if search:
        search_filter = or_(
            CustomerService.base_id.ilike(f"%{search}%"),
            CustomerService.activity.ilike(f"%{search}%"),
            CustomerService.client.ilike(f"%{search}%"),
            CustomerService.contract.ilike(f"%{search}%"),
            CustomerService.type_of_service.ilike(f"%{search}%"),
            CustomerService.status.ilike(f"%{search}%"),
            CustomerService.order_num.ilike(f"%{search}%"),
            CustomerService.first_point.ilike(f"%{search}%"),
            CustomerService.second_point.ilike(f"%{search}%"),
            CustomerService.speed.ilike(f"%{search}%"),
            CustomerService.vlan_id.ilike(f"%{search}%"),
            CustomerService.switchboard_first_point.ilike(f"%{search}%"),
            CustomerService.switch_port_first_point.ilike(f"%{search}%"),
            CustomerService.port_settings_first_point.ilike(f"%{search}%"),
            CustomerService.switchboard_second_point.ilike(f"%{search}%"),
            CustomerService.switch_port_second_point.ilike(f"%{search}%"),
            CustomerService.port_settings_second_point.ilike(f"%{search}%"),
            CustomerService.subnets.ilike(f"%{search}%"),
            CustomerService.router.ilike(f"%{search}%"),
            CustomerService.interface.ilike(f"%{search}%"),
            CustomerService.auto_network.ilike(f"%{search}%"),
            CustomerService.end_client.ilike(f"%{search}%"),
            CustomerService.last_mile.ilike(f"%{search}%"),
            CustomerService.id_servicepipe.ilike(f"%{search}%"),
            CustomerService.comment.ilike(f"%{search}%"),
            CustomerService.responsible_department.ilike(f"%{search}%"),
        )
        query = query.filter(search_filter)
    
    if status:
        query = query.filter(CustomerService.status.ilike(f"%{status}%"))
    
    if client:
        query = query.filter(CustomerService.client.ilike(f"%{client}%"))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    services = query.offset(offset).limit(page_size).all()
    
    return {
        "count": total,
        "results": [service.to_dict() for service in services]
    }


@router.get("/services/{service_id}", response_model=CustomerServiceResponse)
async def get_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get single service by ID"""
    service = db.query(CustomerService).filter(CustomerService.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service.to_dict()


@router.put("/services/{service_id}", response_model=CustomerServiceResponse)
async def update_service(
    service_id: int,
    service_data: CustomerServiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update service information"""
    service = db.query(CustomerService).filter(CustomerService.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Update fields
    update_data = service_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(service, field, value)
    
    db.commit()
    db.refresh(service)
    return service.to_dict()


@router.get("/stats")
async def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get statistics about services"""
    load_csv_to_db(db)
    
    total = db.query(CustomerService).count()
    
    # Count by status
    status_counts = {}
    statuses = db.query(CustomerService.status).distinct().all()
    for (status,) in statuses:
        if status:
            count = db.query(CustomerService).filter(CustomerService.status == status).count()
            status_counts[status] = count
    
    return {
        "total_services": total,
        "status_distribution": status_counts,
    }
