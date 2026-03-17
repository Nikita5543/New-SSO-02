from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.plugins.customer_services.models import CustomerService

router = APIRouter()


def parse_vlan_ids(vlan_string: Optional[str]) -> List[int]:
    """Парсит строку VLAN ID в список чисел.
    Поддерживает форматы: '100', '100;200;300', '100,200,300'
    """
    if not vlan_string:
        return []
    
    vlan_ids = []
    # Разделяем по разделителям (; , или пробел)
    separators = [';', ',', ' ', '|']
    parts = [vlan_string]
    
    for sep in separators:
        new_parts = []
        for part in parts:
            new_parts.extend(part.split(sep))
        parts = new_parts
    
    for part in parts:
        part = part.strip()
        if part.isdigit():
            vlan_id = int(part)
            if 1 <= vlan_id <= 4094:  # Валидный диапазон VLAN
                vlan_ids.append(vlan_id)
    
    return vlan_ids


@router.get("/free-vlans")
async def get_free_vlans(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Получить список свободных VLAN.
    
    VLAN считается занятым, если есть хотя бы одна услуга со статусом 'Эксплуатация'.
    VLAN считается свободным, если все услуги с этим VLAN имеют статус 'Отключен'.
    """
    # Получаем все услуги с VLAN
    services = db.query(CustomerService).filter(
        CustomerService.vlan_id.isnot(None),
        CustomerService.vlan_id != ''
    ).all()
    
    # Собираем информацию о VLAN
    vlan_usage = {}  # vlan_id -> {'active': bool, 'services': []}
    
    for service in services:
        vlan_ids = parse_vlan_ids(service.vlan_id)
        
        for vlan_id in vlan_ids:
            if vlan_id not in vlan_usage:
                vlan_usage[vlan_id] = {
                    'active': False,
                    'services': []
                }
            
            vlan_usage[vlan_id]['services'].append({
                'id': service.id,
                'client': service.client,
                'status': service.status,
                'activity': service.activity
            })
            
            # Если хотя бы одна услуга в эксплуатации - VLAN занят
            if service.status == 'Эксплуатация':
                vlan_usage[vlan_id]['active'] = True
    
    # Фильтруем только свободные VLAN
    free_vlans = []
    for vlan_id, info in vlan_usage.items():
        if not info['active']:  # VLAN свободен
            # Получаем последнюю отключенную услугу для информации
            disabled_services = [s for s in info['services'] if s['status'] == 'Отключен']
            
            free_vlans.append({
                'vlan_id': vlan_id,
                'previous_services': disabled_services,
                'service_count': len(info['services'])
            })
    
    # Сортируем по VLAN ID
    free_vlans.sort(key=lambda x: x['vlan_id'])
    
    # Применяем поиск
    if search:
        search_lower = search.lower()
        free_vlans = [
            v for v in free_vlans
            if search_lower in str(v['vlan_id'])
            or any(search_lower in (s.get('client') or '').lower() for s in v['previous_services'])
        ]
    
    # Пагинация
    total = len(free_vlans)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_vlans = free_vlans[start:end]
    
    return {
        'count': total,
        'results': paginated_vlans,
        'page': page,
        'page_size': page_size
    }


@router.get("/vlan-stats")
async def get_vlan_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Получить статистику по VLAN"""
    services = db.query(CustomerService).filter(
        CustomerService.vlan_id.isnot(None),
        CustomerService.vlan_id != ''
    ).all()
    
    vlan_usage = {}
    
    for service in services:
        vlan_ids = parse_vlan_ids(service.vlan_id)
        
        for vlan_id in vlan_ids:
            if vlan_id not in vlan_usage:
                vlan_usage[vlan_id] = {
                    'active': False,
                    'count': 0
                }
            
            vlan_usage[vlan_id]['count'] += 1
            if service.status == 'Эксплуатация':
                vlan_usage[vlan_id]['active'] = True
    
    total_vlans = len(vlan_usage)
    occupied_vlans = sum(1 for v in vlan_usage.values() if v['active'])
    free_vlans = total_vlans - occupied_vlans
    
    return {
        'total_unique_vlans': total_vlans,
        'occupied_vlans': occupied_vlans,
        'free_vlans': free_vlans
    }


@router.get("/occupied-vlans")
async def get_occupied_vlans(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Получить список занятых VLAN (для справки)"""
    services = db.query(CustomerService).filter(
        CustomerService.vlan_id.isnot(None),
        CustomerService.vlan_id != ''
    ).all()
    
    vlan_usage = {}
    
    for service in services:
        vlan_ids = parse_vlan_ids(service.vlan_id)
        
        for vlan_id in vlan_ids:
            if vlan_id not in vlan_usage:
                vlan_usage[vlan_id] = {
                    'active': False,
                    'services': []
                }
            
            vlan_usage[vlan_id]['services'].append({
                'id': service.id,
                'client': service.client,
                'status': service.status,
                'activity': service.activity
            })
            
            if service.status == 'Эксплуатация':
                vlan_usage[vlan_id]['active'] = True
    
    # Фильтруем только занятые VLAN
    occupied_vlans = [
        {
            'vlan_id': vlan_id,
            'services': info['services'],
            'service_count': len(info['services'])
        }
        for vlan_id, info in vlan_usage.items()
        if info['active']
    ]
    
    occupied_vlans.sort(key=lambda x: x['vlan_id'])
    
    total = len(occupied_vlans)
    start = (page - 1) * page_size
    end = start + page_size
    
    return {
        'count': total,
        'results': occupied_vlans[start:end],
        'page': page,
        'page_size': page_size
    }
