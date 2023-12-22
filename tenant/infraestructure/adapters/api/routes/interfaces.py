from typing import Optional
from fastapi import APIRouter, Depends
from tenant.application.usecases.appliance.network_interfaces.display_brief_network_interface import \
    DisplayBriefNetworkInterface
from tenant.application.usecases.appliance.network_interfaces.display_network_interfaces import DisplayNetworkInterfaces
from tenant.application.usecases.appliance.network_interfaces.no_shutdown_network_interface import \
    NoShutdownNetworkInterface
from tenant.application.usecases.appliance.network_interfaces.set_description_network_interface import \
    SetDescriptionNetworkInterface
from tenant.application.usecases.appliance.network_interfaces.set_ip_network_interface import SetIPNetworkInterface
from tenant.application.usecases.appliance.network_interfaces.shutdown_network_interface import ShutdownNetworkInterface
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.domain.schemas.appliances.network_interfaces.network_interface_brief import NetworkInterfaceBrief
from tenant.domain.models.repository_type import RepositoryType
from tenant.domain.models.role import Role
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.domain.ports.appliances.network_interfaces.interface_set_ip_network_interface import ISetIPNetworkInterface
from tenant.domain.models.role_checker import RoleChecker
from tenant.infraestructure.adapters.appliances.appliance_factory import ApplianceFactory
from tenant.infraestructure.adapters.repositories.factories.node_respository_factory import NodeRepositoryFactory
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance

interfaces_router = APIRouter(prefix="/api/v1/interfaces", tags=["Network interfaces"])

repo_type = RepositoryType.mongo_db_user

allow_access_read = RoleChecker([Role.admin, Role.editor, Role.viewer])
allow_access_edit = RoleChecker([Role.admin, Role.editor])


@interfaces_router.get("/{node_name}", response_model=list[NetworkInterface],
                       dependencies=[Depends(allow_access_read)])
async def interfaces(node_name: str, interface_name: Optional[str] = None) -> list[NetworkInterface]:
    return DisplayNetworkInterfaces(get_appliance(node_name)).display(interface_name)


@interfaces_router.get("/brief/{node_name}", response_model=list[NetworkInterfaceBrief],
                       dependencies=[Depends(allow_access_read)])
async def interfaces_brief(node_name: str) -> list[NetworkInterfaceBrief]:
    return DisplayBriefNetworkInterface(get_appliance(node_name)).display_brief()


@interfaces_router.put("/{node_name}", response_model=NetworkInterface,
                       dependencies=[Depends(allow_access_edit)])
async def set_ip_and_mask(node_name: str, interface: str, ip_and_mask_in_cidr: str) -> NetworkInterface:
    interface_ip: ISetIPNetworkInterface = SetIPNetworkInterface(get_appliance(node_name))
    return interface_ip.set_ip(interface, ip_and_mask_in_cidr)


@interfaces_router.put("/description/{node_name}", response_model=NetworkInterface,
                       dependencies=[Depends(allow_access_edit)])
async def set_description(node_name: str, interface: str, description: str) -> NetworkInterface:
    return SetDescriptionNetworkInterface(get_appliance(node_name)).set_description(interface, description)


@interfaces_router.put("/shutdown/{node_name}", response_model=NetworkInterface,
                       dependencies=[Depends(allow_access_edit)])
async def shutdown_port(node_name: str, interface: str) -> NetworkInterface:
    return ShutdownNetworkInterface(get_appliance(node_name)).shutdown(interface)


@interfaces_router.put("/no-shutdown/{node_name}", response_model=NetworkInterface,
                       dependencies=[Depends(allow_access_edit)])
async def no_shutdown_port(node_name: str, interface: str) -> NetworkInterface:
    return NoShutdownNetworkInterface(get_appliance(node_name)).no_shutdown(interface)


def get_appliance(node_name: str) -> Appliance:
    repository = NodeRepositoryFactory.get_repository(repo_type)
    node: NodeWithCredentials = repository.retrieve_with_credentials(node_name)
    return ApplianceFactory.get_appliance(node)
