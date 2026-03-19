PLUGIN_META = {
    "name": "network_status",
    "version": "1.0.0",
    "description": "Network device monitoring - router status checks",
    "author": "NOC Vision Team",
}


def register(app, context):
    from app.plugins.network_status.endpoints import router

    app.include_router(
        router,
        prefix=context.api_prefix,
        tags=["Network Status"],
    )
