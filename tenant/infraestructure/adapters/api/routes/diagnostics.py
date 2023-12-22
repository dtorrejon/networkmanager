from typing import Optional
from fastapi import APIRouter, Depends

from tenant.application.usecases.appliance.diagnostics.launch_arp import LaunchArp
from tenant.application.usecases.appliance.diagnostics.launch_ping import LaunchPing
from tenant.application.usecases.appliance.diagnostics.launch_trace_route import LaunchTraceRoute
from tenant.domain.schemas.appliances.diagnostics.arp import Arp
from tenant.domain.schemas.appliances.diagnostics.ping import Ping
from tenant.domain.schemas.appliances.diagnostics.ping_command_fields import PingCommandFields
from tenant.domain.schemas.appliances.diagnostics.trace_route import TraceRoute
from tenant.domain.schemas.appliances.diagnostics.trace_route_command_fields import TraceRouteCommandFields
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.domain.ports.appliances.diagnostics.interface_launch_arp import ILaunchArp
from tenant.domain.ports.appliances.diagnostics.interface_launch_ping import ILaunchPing
from tenant.domain.ports.appliances.diagnostics.interface_launch_traceroute import ILaunchTraceRoute
from tenant.domain.models.repository_type import RepositoryType
from tenant.domain.models.role_checker import RoleChecker
from tenant.domain.models.role import Role
from tenant.infraestructure.adapters.appliances.appliance_factory import ApplianceFactory
from tenant.infraestructure.adapters.repositories.factories.node_respository_factory import NodeRepositoryFactory

diagnostics_router = APIRouter(prefix="/api/v1/diagnostics", tags=["Diagnostics"])

repo_node = NodeRepositoryFactory.get_repository(RepositoryType.mongo_db_user)

allow_access_read = RoleChecker([Role.admin, Role.editor, Role.viewer])


@diagnostics_router.get("/ping/{node_name}/{destination_ip}", response_model=Ping,
                        dependencies=[Depends(allow_access_read)])
async def ping(node_name: str, destination_ip: str, source_ip: Optional[str] = None, repeat_ping: int = 4) -> Ping:
    ping_command_fields: PingCommandFields = PingCommandFields(sourceIpAddress=source_ip,
                                                               destinationIpAddress=destination_ip, repeat=repeat_ping)
    node: NodeWithCredentials = repo_node.retrieve_with_credentials(node_name)
    appliance = ApplianceFactory.get_appliance(node)
    launch_ping: ILaunchPing = LaunchPing(appliance)
    return launch_ping.ping(ping_command_fields)


@diagnostics_router.get("/traceroute/{node_name}/{destination_ip}", response_model=TraceRoute,
                        dependencies=[Depends(allow_access_read)])
async def trace_route(node_name: str, destination_ip: str, source_ip: Optional[str] = None,
                      probe_count: int = 3) -> TraceRoute:
    trace_route_command_fields: TraceRouteCommandFields = TraceRouteCommandFields(sourceIpAddress=source_ip,
                                                                                  destinationIpAddress=destination_ip,
                                                                                  probeCount=probe_count)

    node: NodeWithCredentials = repo_node.retrieve_with_credentials(node_name)
    appliance = ApplianceFactory.get_appliance(node)
    launch_trace_route: ILaunchTraceRoute = LaunchTraceRoute(appliance)
    return launch_trace_route.trace_route(trace_route_command_fields)


@diagnostics_router.get("/arp/{node_name}", response_model=list[Arp], dependencies=[Depends(allow_access_read)])
async def arp(node_name: str)-> list[Arp]:
    node: NodeWithCredentials = repo_node.retrieve_with_credentials(node_name)
    appliance = ApplianceFactory.get_appliance(node)
    launch_arp: ILaunchArp = LaunchArp(appliance)
    return launch_arp.arp()


