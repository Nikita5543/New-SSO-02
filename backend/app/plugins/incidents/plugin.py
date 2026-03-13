PLUGIN_META = {
    "name": "incidents",
    "version": "1.0.0",
    "description": "Incident management - create, track, and resolve network incidents",
    "author": "NOC Vision Team",
}


def register(app, context):
    from app.plugins.incidents.endpoints import router

    app.include_router(
        router,
        prefix=context.api_prefix,
        tags=["Incidents"],
    )
