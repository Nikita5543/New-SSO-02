PLUGIN_META = {
    "name": "configuration",
    "version": "1.0.0",
    "description": "Configuration management - snapshots, templates, change tracking",
    "author": "NOC Vision Team",
}


def register(app, context):
    from app.plugins.configuration.endpoints import router

    app.include_router(
        router,
        prefix=context.api_prefix,
        tags=["Configuration"],
    )
