from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
import httpx
from app.core.config import settings

router = APIRouter()


async def get_netbox_data(endpoint: str, params: Optional[dict] = None):
    """Получить данные из NetBox API"""
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


@router.get("/devices")
async def list_devices(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    q: Optional[str] = None,
    ordering: Optional[str] = None
):
    """
    Получить список устройств из NetBox DCIM.
    
    Параметры:
    - page: Номер страницы
    - page_size: Количество элементов (1-100)
    - q: Поиск по имени устройства
    - ordering: Сортировка (name, -name, status, etc.)
    """
    params = {
        "limit": page_size,
        "offset": (page - 1) * page_size,
    }
    
    if q:
        params["q"] = q
    if ordering:
        params["ordering"] = ordering
    
    try:
        data = await get_netbox_data("dcim/devices/", params)
        
        # Преобразовать данные в формат frontend
        results = []
        for item in data.get("results", []):
            results.append({
                "id": item.get("id"),
                "name": item.get("name"),
                "status": item.get("status"),
                "site": item.get("site"),
                "location": item.get("location"),
                "rack": item.get("rack"),
                "role": item.get("role"),
                "device_type": item.get("device_type"),
                "primary_ip": item.get("primary_ip"),
                "primary_ip4": item.get("primary_ip4"),
                "description": item.get("description"),
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
