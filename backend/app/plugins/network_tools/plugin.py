PLUGIN_META = {
    "name": "network_tools",
    "version": "1.0.0",
    "description": "Network tools - internal and external resources",
    "author": "NOC Vision Team",
}


def register(app, context):
    """Register network tools plugin"""
    from app.plugins.network_tools.endpoints import router

    app.include_router(
        router,
        prefix=context.api_prefix,
        tags=["Network Tools"],
    )
