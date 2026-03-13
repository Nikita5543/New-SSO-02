PLUGIN_META = {
    "name": "performance",
    "version": "1.0.0",
    "description": "Network performance monitoring - targets, metrics, thresholds",
    "author": "NOC Vision Team",
}


def register(app, context):
    from app.plugins.performance.endpoints import router

    app.include_router(
        router,
        prefix=context.api_prefix,
        tags=["Performance"],
    )
