from fastapi import APIRouter, Depends
from typing import List

from app.core.security import get_current_active_user
from app.models.user import User

router = APIRouter()

# Internal tools configuration
INTERNAL_TOOLS = [
    {"name": "NetBox", "url": "http://10.100.22.11:8000/", "description": "IPAM and DCIM"},
    {"name": "LibreNMS", "url": "https://librenms.cirex.ru/", "description": "Network monitoring"},
    {"name": "ServiceBase", "url": "https://servicebase.cirex.ru/", "description": "Service management"},
    {"name": "Zabbix", "url": "http://10.100.22.22/zabbix.php?action=dashboard.view&dashboardid=1", "description": "Infrastructure monitoring"},
    {"name": "Wiki-NOC", "url": "https://wiki-dev.cirex.ru/spaces/NOC/pages/18415670/NOC", "description": "NOC documentation"},
    {"name": "Jira-SPD", "url": "https://jira-dev.cirex.ru/secure/Dashboard.jspa", "description": "Project management"},
    {"name": "Grafana", "url": "http://zabbix.svcp.io:3000/d/Z5k7NFdMk/cirex-upstreams?orgId=1&from=now-6h&to=now&timezone=browser&refresh=10s", "description": "Dashboards and metrics"},
    {"name": "LG", "url": "https://lg.cirex.ru/", "description": "Looking Glass"},
]

# External tools configuration
EXTERNAL_TOOLS = [
    {"name": "RIPE Database", "url": "https://apps.db.ripe.net/db-web-ui/query", "description": "RIPE WHOIS database"},
    {"name": "Whois", "url": "https://whois.icann.org/", "description": "ICANN WHOIS lookup"},
]


@router.get("/internal-tools")
async def get_internal_tools(
    current_user: User = Depends(get_current_active_user),
):
    """Get list of internal network tools"""
    return {"tools": INTERNAL_TOOLS}


@router.get("/external-tools")
async def get_external_tools(
    current_user: User = Depends(get_current_active_user),
):
    """Get list of external network tools"""
    return {"tools": EXTERNAL_TOOLS}
