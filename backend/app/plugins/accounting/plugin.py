PLUGIN_META = {
    "name": "accounting",
    "version": "1.0.0",
    "description": "Traffic accounting - interfaces, traffic records, bandwidth usage",
    "author": "NOC Vision Team",
}


def register(app, context):
    from app.plugins.accounting.endpoints import router

    app.include_router(
        router,
        prefix=context.api_prefix,
        tags=["Accounting"],
    )
