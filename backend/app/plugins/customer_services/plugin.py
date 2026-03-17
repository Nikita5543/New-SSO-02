PLUGIN_META = {
    "name": "customer_services",
    "version": "1.0.0",
    "description": "Customer services management - view and edit service database",
    "author": "NOC Vision Team",
}


def register(app, context):
    from app.plugins.customer_services.endpoints import router

    app.include_router(
        router,
        prefix=context.api_prefix,
        tags=["Customer Services"],
    )
