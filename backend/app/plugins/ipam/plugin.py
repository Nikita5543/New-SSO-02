PLUGIN_META = {
    "name": "ipam",
    "version": "1.0.0",
    "description": "NetBox IPAM integration - validate and manage IP addresses",
    "author": "NOC Vision Team",
}


def register(app, context):
    from app.plugins.ipam.endpoints import router

    app.include_router(
        router,
        prefix=context.api_prefix,
        tags=["IPAM"],
    )
