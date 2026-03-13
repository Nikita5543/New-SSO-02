PLUGIN_META = {
    "name": "security",
    "version": "1.0.0",
    "description": "Security module - audit logs, security events, access monitoring",
    "author": "NOC Vision Team",
}


def register(app, context):
    from app.plugins.security_module.endpoints import router

    app.include_router(
        router,
        prefix=context.api_prefix,
        tags=["Security"],
    )
