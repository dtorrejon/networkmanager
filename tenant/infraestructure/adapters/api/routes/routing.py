from fastapi import APIRouter, Depends
from tenant.application.usecases.appliance.routing.launch_routing_table import LaunchRoutingTable
from tenant.application.usecases.appliance.routing.set_default_gateway import SetDefaultGateway
from tenant.application.usecases.appliance.routing.set_static_route import SetStaticRoute
from tenant.domain.models.repository_type import RepositoryType
from tenant.domain.models.role import Role
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.domain.ports.appliances.routing.interface_launch_routing_table import ILaunchRoutingTable
from tenant.domain.ports.appliances.routing.interface_set_default_gateway import ISetDefaultGateway
from tenant.domain.ports.appliances.routing.interface_set_static_route import ISetStaticRoute
from tenant.domain.models.role_checker import RoleChecker
from tenant.domain.schemas.appliances.diagnostics.route import Route
from tenant.infraestructure.adapters.appliances.appliance_factory import ApplianceFactory
from tenant.infraestructure.adapters.repositories.factories.node_respository_factory import NodeRepositoryFactory

routing_router = APIRouter(prefix="/api/v1/routing", tags=["Routing"])

repo_node = NodeRepositoryFactory.get_repository(RepositoryType.mongo_db_user)

allow_access_edit = RoleChecker([Role.admin, Role.editor])
allow_access_read = RoleChecker([Role.admin, Role.editor, Role.viewer])


@routing_router.get("/routing-table/{node_name}", response_model=list[Route],
                    dependencies=[Depends(allow_access_read)])
async def routing_table(node_name: str) -> list[Route]:
    node: NodeWithCredentials = repo_node.retrieve_with_credentials(node_name)
    appliance = ApplianceFactory.get_appliance(node)
    launch_routing_table: ILaunchRoutingTable = LaunchRoutingTable(appliance)
    return launch_routing_table.routing_table()


@routing_router.post("/static/{node_name}", response_model=list[Route],
                     dependencies=[Depends(allow_access_edit)])
async def static_route(node_name: str, ip_and_mask_in_cidr: str, next_hop: str) -> list[Route]:
    node: NodeWithCredentials = repo_node.retrieve_with_credentials(node_name)
    appliance = ApplianceFactory.get_appliance(node)
    set_static_route: ISetStaticRoute = SetStaticRoute(appliance)
    return set_static_route.set_static_route(ip_and_mask_in_cidr, next_hop)


@routing_router.post("/static/default/{node_name}", response_model=list[Route],
                     dependencies=[Depends(allow_access_edit)])
async def default_gateway(node_name: str, ip: str) -> list[Route]:
    node: NodeWithCredentials = repo_node.retrieve_with_credentials(node_name)
    appliance = ApplianceFactory.get_appliance(node)
    set_default_gateway: ISetDefaultGateway = SetDefaultGateway(appliance)
    return set_default_gateway.set_default_gateway(ip)
