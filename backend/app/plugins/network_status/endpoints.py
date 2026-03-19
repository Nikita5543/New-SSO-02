import subprocess
import httpx
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.core.config import settings
from app.models.user import User
from app.plugins.network_status.models import NetworkDevice, DeviceCheckResult
from app.plugins.network_status.schemas import (
    NetworkDeviceResponse,
    DeviceCheckResultResponse,
    DeviceWithLatestCheck,
    DeviceStatusListResponse,
    CheckRunResponse,
)

router = APIRouter()

# NetBox configuration from settings
NETBOX_URL = settings.NETBOX_URL
NETBOX_TOKEN = settings.NETBOX_TOKEN


async def get_netbox_routers() -> List[dict]:
    """Fetch routers from NetBox API"""
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Token {NETBOX_TOKEN}",
                "Content-Type": "application/json",
            }
            # Get devices with role=router
            response = await client.get(
                f"{NETBOX_URL}/dcim/devices/",
                headers=headers,
                params={"role": "router", "status": "active"},
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
    except Exception as e:
        print(f"Error fetching from NetBox: {e}")
        return []


async def sync_devices_from_netbox(db: Session):
    """Sync router devices from NetBox to local DB"""
    routers = await get_netbox_routers()
    
    for router in routers:
        netbox_id = router.get("id")
        existing = db.query(NetworkDevice).filter(
            NetworkDevice.netbox_id == netbox_id
        ).first()
        
        device_data = {
            "netbox_id": netbox_id,
            "hostname": router.get("name", ""),
            "mgmt_ip": router.get("primary_ip4", {}).get("address", "").split("/")[0] if router.get("primary_ip4") else "",
            "platform": router.get("platform", {}).get("name", ""),
            "device_role": router.get("device_role", {}).get("name", ""),
            "site": router.get("site", {}).get("name", ""),
            "status": router.get("status", "active"),
        }
        
        if existing:
            for key, value in device_data.items():
                setattr(existing, key, value)
        else:
            new_device = NetworkDevice(**device_data)
            db.add(new_device)
    
    db.commit()
    return len(routers)


def run_check_script(device_id: int, mgmt_ip: str, hostname: str):
    """
    Run external Python script to check device status.
    This runs in background.
    """
    # TODO: Path to script will be configured by user
    script_path = os.getenv("DEVICE_CHECK_SCRIPT", "/opt/scripts/check_device.py")
    
    try:
        result = subprocess.run(
            ["python3", script_path, mgmt_ip, hostname],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes timeout
        )
        
        # Parse JSON output from script
        import json
        if result.returncode == 0:
            output = json.loads(result.stdout)
            return {
                "status": "completed",
                "operational_status": output.get("operational_status", "Unknown"),
                "backup_status": output.get("backup_status", "NONE"),
                "snapshot_status": output.get("snapshot_status", "NONE"),
                "critical_alarm": output.get("critical_alarm", "NO"),
                "raw_output": result.stdout,
            }
        else:
            return {
                "status": "failed",
                "error_message": result.stderr or "Script failed",
                "raw_output": result.stdout,
            }
    except subprocess.TimeoutExpired:
        return {
            "status": "failed",
            "error_message": "Script timeout (5 minutes)",
        }
    except Exception as e:
        return {
            "status": "failed",
            "error_message": str(e),
        }


@router.get("/devices", response_model=DeviceStatusListResponse)
async def list_devices_with_status(
    sync: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    List all network devices with their latest check status.
    If sync=True, sync devices from NetBox first.
    """
    if sync:
        await sync_devices_from_netbox(db)
    
    devices = db.query(NetworkDevice).all()
    
    result = []
    for device in devices:
        # Get latest check result
        latest_check = db.query(DeviceCheckResult).filter(
            DeviceCheckResult.device_id == device.id
        ).order_by(desc(DeviceCheckResult.check_date)).first()
        
        result.append(DeviceWithLatestCheck(
            device=device.to_dict(),
            latest_check=latest_check.to_dict() if latest_check else None
        ))
    
    # Calculate summary
    total = len(devices)
    online = sum(1 for r in result if r.latest_check and r.latest_check.operational_status == "Online")
    offline = sum(1 for r in result if r.latest_check and r.latest_check.operational_status == "Offline")
    backup_ok = sum(1 for r in result if r.latest_check and r.latest_check.backup_status == "OK")
    backup_failed = sum(1 for r in result if r.latest_check and r.latest_check.backup_status == "Failed")
    critical_yes = sum(1 for r in result if r.latest_check and r.latest_check.critical_alarm == "YES")
    
    return DeviceStatusListResponse(
        devices=result,
        total=total,
        summary={
            "operational": {"online": online, "offline": offline, "total": total},
            "backup": {"ok": backup_ok, "failed": backup_failed, "total": total},
            "critical": {"yes": critical_yes, "total": total},
        }
    )


@router.post("/devices/{device_id}/check", response_model=CheckRunResponse)
async def run_device_check(
    device_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Start a status check for a specific device"""
    device = db.query(NetworkDevice).filter(NetworkDevice.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Create pending check record
    check = DeviceCheckResult(
        device_id=device_id,
        check_status="running",
    )
    db.add(check)
    db.commit()
    db.refresh(check)
    
    # Run check in background
    # TODO: Implement actual background task
    # For now, just return the check ID
    
    return CheckRunResponse(
        check_id=check.id,
        device_id=device_id,
        status="running",
        message=f"Check started for {device.hostname}",
    )


@router.post("/devices/check-all")
async def run_check_all(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Start status check for all devices"""
    devices = db.query(NetworkDevice).all()
    
    check_ids = []
    for device in devices:
        check = DeviceCheckResult(
            device_id=device.id,
            check_status="pending",
        )
        db.add(check)
        check_ids.append(check.id)
    
    db.commit()
    
    return {
        "status": "started",
        "total_devices": len(devices),
        "check_ids": check_ids,
        "message": f"Started checks for {len(devices)} devices",
    }


@router.get("/devices/{device_id}/history", response_model=List[DeviceCheckResultResponse])
async def get_device_check_history(
    device_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get check history for a specific device"""
    checks = db.query(DeviceCheckResult).filter(
        DeviceCheckResult.device_id == device_id
    ).order_by(desc(DeviceCheckResult.check_date)).limit(limit).all()
    
    return [check.to_dict() for check in checks]


@router.post("/sync-from-netbox")
async def sync_devices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Manually sync devices from NetBox"""
    count = await sync_devices_from_netbox(db)
    return {"status": "success", "synced_devices": count}
