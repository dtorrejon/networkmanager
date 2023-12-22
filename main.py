from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from tenant.infraestructure.adapters.api.routes import users, tenant, authentication, nodes, compatible_nodes, \
    diagnostics, system, interfaces, routing, commands, vlans, svi




def update_api_schema():
    DOC_TITLE = f"Network Manager API Documentation"
    DOC_VERSION = "1.0"
    openapi_schema = get_openapi(title=DOC_TITLE, version=DOC_VERSION, routes=app.routes, )

    openapi_schema["info"] = {
        "title": DOC_TITLE,
        "version": DOC_VERSION,
        "description": "This application is a prototype.",
        "contact": {
            "name": "David Torrejón Vázquez",
            "url": "https://www.linkedin.com/in/david-torrejon/",
            "email": "david.torrejon.vazquez@gmail.com"
        },
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
        },
    }
    app.openapi_schema = openapi_schema

    return openapi_schema


app = FastAPI(prefix="/api", swagger_ui_parameters={"defaultModelsExpandDepth": -1})


app.include_router(authentication.auth_router)
app.include_router(tenant.tenant_router)
app.include_router(users.users_router)
app.include_router(nodes.nodes_router)
app.include_router(compatible_nodes.compatible_nodes_router)
app.include_router(system.system_router)
app.include_router(diagnostics.diagnostics_router)
app.include_router(interfaces.interfaces_router)
app.include_router(vlans.vlan_router)
app.include_router(svi.svi_router)
app.include_router(routing.routing_router)
app.include_router(commands.commands_router)

update_api_schema()
