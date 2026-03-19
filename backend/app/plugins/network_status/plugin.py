from fastapi import APIRouter
from app.plugins.network_status.endpoints import router


def register():
    """Register network status plugin"""
    return {
        "name": "network_status",
        "label": "Network Status",
        "section": "analytics",
        "version": "1.0.0",
        "router": router,
        "models": ["NetworkDevice", "DeviceCheckResult"],
    }
