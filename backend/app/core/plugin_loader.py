import importlib
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Base, get_db
from app.core.security import get_current_active_user, get_current_admin_user

logger = logging.getLogger(__name__)


@dataclass
class PluginContext:
    db_base: type
    api_prefix: str
    get_db: Callable
    get_current_user: Callable
    get_current_admin_user: Callable


def load_plugins(app: FastAPI) -> List[dict]:
    plugins_dir = Path(__file__).parent.parent / "plugins"
    loaded = []

    if not plugins_dir.exists():
        logger.warning(f"Plugins directory not found: {plugins_dir}")
        return loaded

    # Filter by enabled plugins if configured
    enabled = None
    if settings.ENABLED_PLUGINS:
        enabled = [p.strip() for p in settings.ENABLED_PLUGINS.split(",") if p.strip()]

    for item in sorted(plugins_dir.iterdir()):
        if not item.is_dir():
            continue
        if item.name.startswith("_"):
            continue
        if not (item / "plugin.py").exists():
            continue

        if enabled is not None and item.name not in enabled:
            logger.info(f"Plugin '{item.name}' skipped (not in ENABLED_PLUGINS)")
            continue

        try:
            # Import models first to register them on Base.metadata
            try:
                importlib.import_module(f"app.plugins.{item.name}.models")
            except ImportError:
                pass  # Plugin may not have models

            # Import the plugin module
            plugin_module = importlib.import_module(f"app.plugins.{item.name}.plugin")

            meta = getattr(plugin_module, "PLUGIN_META", None)
            register_fn = getattr(plugin_module, "register", None)

            if not meta or not register_fn:
                logger.warning(
                    f"Plugin '{item.name}' missing PLUGIN_META or register()"
                )
                continue

            plugin_name = meta.get("name", item.name)
            context = PluginContext(
                db_base=Base,
                api_prefix=f"/api/v1/plugins/{plugin_name}",
                get_db=get_db,
                get_current_user=get_current_active_user,
                get_current_admin_user=get_current_admin_user,
            )

            register_fn(app, context)

            plugin_info = {
                "name": plugin_name,
                "version": meta.get("version", "1.0.0"),
                "description": meta.get("description", ""),
                "status": "loaded",
            }
            loaded.append(plugin_info)
            logger.info(f"Plugin '{plugin_name}' loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load plugin '{item.name}': {e}", exc_info=True)
            loaded.append({
                "name": item.name,
                "version": "unknown",
                "description": "",
                "status": "error",
                "error": str(e),
            })

    return loaded
