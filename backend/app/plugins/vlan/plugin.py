PLUGIN_META = {
    "name": "vlan",
    "version": "1.0.0",
    "description": "VLAN management - free and occupied VLAN database",
    "author": "NOC Vision Team",
}


def register(app, context):
    from app.plugins.vlan.endpoints import router

    app.include_router(
        router,
        prefix=context.api_prefix,
        tags=["VLAN"],
    )
