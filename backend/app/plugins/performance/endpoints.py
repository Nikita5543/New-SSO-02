import os
import subprocess
import psutil
from typing import List, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.plugins.performance.models import MonitorTarget, MetricSample
from app.plugins.performance.schemas import MonitorTargetCreate, MonitorTargetResponse, MetricSampleResponse

router = APIRouter()


def get_docker_containers():
    """Get Docker container statuses"""
    try:
        result = subprocess.run(
            ['docker', 'ps', '-a', '--format', '{{.Names}}|{{.Status}}|{{.Image}}'],
            capture_output=True, text=True, timeout=10
        )
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('|')
                if len(parts) >= 2:
                    name = parts[0]
                    status = parts[1]
                    image = parts[2] if len(parts) > 2 else ''
                    
                    # Parse status
                    if 'Up' in status:
                        state = 'running'
                        health = 'healthy' if 'healthy' in status else 'unknown'
                    elif 'Exited' in status:
                        state = 'stopped'
                        health = 'unhealthy'
                    else:
                        state = 'unknown'
                        health = 'unknown'
                    
                    containers.append({
                        'name': name,
                        'state': state,
                        'health': health,
                        'status': status,
                        'image': image
                    })
        return containers
    except Exception as e:
        return [{'name': 'docker-error', 'state': 'error', 'health': 'unknown', 'status': str(e), 'image': ''}]


def get_system_metrics():
    """Get system metrics (CPU, RAM, Disk)"""
    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        # Memory
        memory = psutil.virtual_memory()
        
        # Disk
        disk = psutil.disk_usage('/')
        
        # Network
        net_io = psutil.net_io_counters()
        
        # Load average (Linux only)
        try:
            load_avg = os.getloadavg()
        except:
            load_avg = [0, 0, 0]
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count,
                'frequency_mhz': cpu_freq.current if cpu_freq else 0,
                'load_avg_1m': load_avg[0],
                'load_avg_5m': load_avg[1],
                'load_avg_15m': load_avg[2],
            },
            'memory': {
                'total_gb': round(memory.total / (1024**3), 2),
                'available_gb': round(memory.available / (1024**3), 2),
                'used_gb': round(memory.used / (1024**3), 2),
                'percent': memory.percent,
            },
            'disk': {
                'total_gb': round(disk.total / (1024**3), 2),
                'used_gb': round(disk.used / (1024**3), 2),
                'free_gb': round(disk.free / (1024**3), 2),
                'percent': round((disk.used / disk.total) * 100, 1),
            },
            'network': {
                'bytes_sent_mb': round(net_io.bytes_sent / (1024**2), 2),
                'bytes_recv_mb': round(net_io.bytes_recv / (1024**2), 2),
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
            }
        }
    except Exception as e:
        return {'error': str(e)}


def get_alarms():
    """Generate alarms based on system state"""
    alarms = []
    
    try:
        # Check CPU
        cpu = psutil.cpu_percent(interval=0.5)
        if cpu > 90:
            alarms.append({
                'level': 'critical',
                'title': 'High CPU Usage',
                'message': f'CPU usage is {cpu}%, consider scaling resources',
                'timestamp': datetime.utcnow().isoformat()
            })
        elif cpu > 70:
            alarms.append({
                'level': 'warning',
                'title': 'Elevated CPU Usage',
                'message': f'CPU usage is {cpu}%',
                'timestamp': datetime.utcnow().isoformat()
            })
        
        # Check Memory
        memory = psutil.virtual_memory()
        if memory.percent > 90:
            alarms.append({
                'level': 'critical',
                'title': 'High Memory Usage',
                'message': f'Memory usage is {memory.percent}% ({round(memory.used/1024**3, 1)}GB used)',
                'timestamp': datetime.utcnow().isoformat()
            })
        elif memory.percent > 80:
            alarms.append({
                'level': 'warning',
                'title': 'Elevated Memory Usage',
                'message': f'Memory usage is {memory.percent}%',
                'timestamp': datetime.utcnow().isoformat()
            })
        
        # Check Disk
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        if disk_percent > 90:
            alarms.append({
                'level': 'critical',
                'title': 'Low Disk Space',
                'message': f'Disk is {disk_percent:.1f}% full',
                'timestamp': datetime.utcnow().isoformat()
            })
        elif disk_percent > 80:
            alarms.append({
                'level': 'warning',
                'title': 'Disk Space Warning',
                'message': f'Disk is {disk_percent:.1f}% full',
                'timestamp': datetime.utcnow().isoformat()
            })
        
        # Check Docker containers
        containers = get_docker_containers()
        stopped = [c for c in containers if c['state'] == 'stopped']
        for container in stopped:
            alarms.append({
                'level': 'critical',
                'title': 'Container Stopped',
                'message': f'Container {container["name"]} is not running',
                'timestamp': datetime.utcnow().isoformat()
            })
        
    except Exception as e:
        alarms.append({
            'level': 'warning',
            'title': 'Monitoring Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        })
    
    return alarms


@router.get("/targets", response_model=List[MonitorTargetResponse])
def list_targets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return db.query(MonitorTarget).all()


@router.post("/targets", response_model=MonitorTargetResponse)
def create_target(
    data: MonitorTargetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    target = MonitorTarget(**data.model_dump())
    db.add(target)
    db.commit()
    db.refresh(target)
    return target


@router.get("/targets/{target_id}", response_model=MonitorTargetResponse)
def get_target(
    target_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    target = db.query(MonitorTarget).filter(MonitorTarget.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Monitor target not found")
    return target


@router.delete("/targets/{target_id}")
def delete_target(
    target_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    target = db.query(MonitorTarget).filter(MonitorTarget.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Monitor target not found")
    db.delete(target)
    db.commit()
    return {"status": "ok", "message": "Target deleted"}


@router.get("/metrics/{target_id}", response_model=List[MetricSampleResponse])
def get_metrics(
    target_id: int,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return (
        db.query(MetricSample)
        .filter(MetricSample.target_id == target_id)
        .order_by(MetricSample.collected_at.desc())
        .limit(limit)
        .all()
    )


@router.get("/system/metrics")
def system_metrics(
    current_user: User = Depends(get_current_active_user),
):
    """Get real-time system metrics (CPU, RAM, Disk, Network)"""
    return get_system_metrics()


@router.get("/system/containers")
def container_status(
    current_user: User = Depends(get_current_active_user),
):
    """Get Docker container statuses"""
    return get_docker_containers()


@router.get("/system/alarms")
def system_alarms(
    current_user: User = Depends(get_current_active_user),
):
    """Get active system alarms"""
    return get_alarms()


@router.get("/system/overview")
def system_overview(
    current_user: User = Depends(get_current_active_user),
):
    """Get complete system overview for dashboard"""
    return {
        'metrics': get_system_metrics(),
        'containers': get_docker_containers(),
        'alarms': get_alarms(),
        'timestamp': datetime.utcnow().isoformat()
    }
