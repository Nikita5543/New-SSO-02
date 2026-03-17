from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import httpx
from app.core.config import settings

router = APIRouter()


class ValidationChange(BaseModel):
    type: str  # 'added' or 'removed'
    interface: str
    device: str
    ip: str
    description: str


class ApplyRequest(BaseModel):
    changes: List[ValidationChange]


async def get_netbox_data(endpoint: str, params: Optional[Dict] = None):
    """
    Получить данные из NetBox API.
    
    Args:
        endpoint: Endpoint относительно базового URL (например, 'ipam/ip-addresses/')
        params: Параметры запроса
    
    Returns:
        JSON ответ от NetBox
    """
    url = f"{settings.NETBOX_URL.rstrip('/')}/{endpoint.lstrip('/')}"
    
    headers = {
        "Authorization": f"Bearer {settings.NETBOX_TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, headers=headers, params=params)
        
        if response.status_code == 401:
            raise HTTPException(status_code=500, detail="NetBox authentication failed")
        elif response.status_code == 403:
            raise HTTPException(status_code=500, detail="NetBox permission denied")
        elif response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"NetBox API error: {response.status_code} - {response.text[:200]}"
            )
        
        return response.json()


@router.post("/validate")
async def validate_ipam():
    """
    Запускает скрипт валидации на удаленной ВМ.
    Возвращает разницу между NetBox и реальным оборудованием.
    
    TODO: Реализовать вызов скрипта на удаленной ВМ
    """
    # Заглушка - в реальности здесь будет вызов скрипта
    return {
        "added": [
            {
                "interface": "ge-0/0/1",
                "device": "juniper-sw1",
                "ip": "192.168.1.10/24",
                "description": "New device"
            }
        ],
        "removed": [
            {
                "interface": "ge-0/0/2",
                "device": "juniper-sw1",
                "ip": "192.168.1.20/24",
                "description": "Old device"
            }
        ]
    }


@router.post("/apply")
async def apply_changes(request: ApplyRequest):
    """
    Применяет изменения в NetBox.
    
    TODO: Реализовать отправку данных в NetBox API
    """
    # Заглушка - в реальности здесь будет отправка в NetBox
    print(f"Applying {len(request.changes)} changes...")
    return {"status": "success", "applied": len(request.changes)}


@router.get("/database")
async def get_database(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    q: Optional[str] = None,
    ordering: Optional[str] = None,
    vrf_id: Optional[str] = None,
    status: Optional[str] = None
):
    """
    Получает все IP адреса из NetBox API.
    
    Поддерживаемые параметры:
    - page: Номер страницы
    - page_size: Количество элементов на странице (1-100)
    - q: Поиск по всем полям
    - ordering: Сортировка (prefix: 'field', desc: '-field')
    - vrf_id: Фильтр по VRF
    - status: Фильтр по статусу
    """
    params = {
        "limit": page_size,
        "offset": (page - 1) * page_size,
    }
    
    # Добавить фильтры
    if q:
        params["q"] = q
    if vrf_id:
        params["vrf_id"] = vrf_id
    if status:
        params["status"] = status
    if ordering:
        params["ordering"] = ordering
    
    try:
        data = await get_netbox_data("ipam/ip-addresses/", params)
        
        # Преобразовать данные в формат frontend
        results = []
        for item in data.get("results", []):
            # Извлечь интерфейс, если есть
            interface_name = "N/A"
            if item.get("assigned_object"):
                assigned_obj = item["assigned_object"]
                interface_name = assigned_obj.get("name", "N/A")
            
            results.append({
                "id": item.get("id"),
                "address": item.get("address"),
                "vrf": item.get("vrf") or {"name": "Global"},
                "status": item.get("status"),
                "vlan": item.get("vlan") or {"vid": "N/A"},
                "description": item.get("description", ""),
                "interface": {"name": interface_name}
            })
        
        return {
            "count": data.get("count", 0),
            "next": data.get("next"),
            "previous": data.get("previous"),
            "results": results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching data from NetBox: {str(e)}"
        )
