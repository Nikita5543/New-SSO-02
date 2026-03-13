PLUGIN_META = {
    "name": "inventory",
    "version": "1.0.0",
    "description": "Equipment inventory management - devices, sites, device types",
    "author": "NOC Vision Team",
}


def register(app, context):
    from app.plugins.inventory.endpoints import router

    app.include_router(
        router,
        prefix=context.api_prefix,
        tags=["Inventory"],
    )
