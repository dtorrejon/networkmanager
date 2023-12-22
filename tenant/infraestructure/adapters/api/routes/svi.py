from fastapi import APIRouter, Depends

from tenant.application.usecases.appliance.svi.create_svi import CreateSVI
from tenant.application.usecases.appliance.svi.delete_svi import DeleteSVI
from tenant.application.usecases.appliance.network_interfaces.no_shutdown_network_interface import \
    NoShutdownNetworkInterface
from tenant.application.usecases.appliance.svi.set_svi_ip import SetSviIp
from tenant.application.usecases.appliance.network_interfaces.shutdown_network_interface import ShutdownNetworkInterface
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.domain.models.repository_type import RepositoryType
from tenant.domain.models.role import Role
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.domain.ports.appliances.network_interfaces.interface_delete_svi import IDeleteSVI
from tenant.domain.ports.appliances.network_interfaces.interface_set_svi_ip import ISetSviIp
from tenant.domain.models.role_checker import RoleChecker
from tenant.infraestructure.adapters.appliances.appliance_factory import ApplianceFactory
from tenant.infraestructure.adapters.repositories.factories.node_respository_factory import NodeRepositoryFactory
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance

svi_router = APIRouter(prefix="/api/v1/svi", tags=["SVI's (Switch Vlan Interfaces)"])

repo_type = RepositoryType.mongo_db_user

allow_access_read = RoleChecker([Role.admin, Role.editor, Role.viewer])
allow_access_edit = RoleChecker([Role.admin, Role.editor])


@svi_router.post("/{node_name}", response_model=NetworkInterface,
                 dependencies=[Depends(allow_access_edit)])
async def create_svi(node_name: str, vlan_id: str) -> NetworkInterface:
    return CreateSVI(get_appliance(node_name)).create(vlan_id)


@svi_router.put("/ip/{node_name}", response_model=NetworkInterface,
                dependencies=[Depends(allow_access_edit)])
async def set_svi_ip_and_mask(node_name: str, svi: str, ip_and_mask_in_cidr: str) -> NetworkInterface:
    interface_ip: ISetSviIp = SetSviIp(get_appliance(node_name))
    return interface_ip.set_svi_ip(svi, ip_and_mask_in_cidr)


@svi_router.delete("/{node_name}", response_model=list[NetworkInterface],
                   dependencies=[Depends(allow_access_edit)])
async def delete_svi(node_name: str, vlan_id: str) -> list[NetworkInterface]:
    svi: IDeleteSVI = DeleteSVI(get_appliance(node_name))
    return svi.delete(vlan_id)


@svi_router.put("/shutdown/{node_name}", response_model=NetworkInterface,
                dependencies=[Depends(allow_access_edit)])
async def shutdown_svi(node_name: str, svi: str) -> NetworkInterface:
    return ShutdownNetworkInterface(get_appliance(node_name)).shutdown(svi)


@svi_router.put("/no-shutdown/{node_name}", response_model=NetworkInterface,
                dependencies=[Depends(allow_access_edit)])
async def no_shutdown_svi(node_name: str, svi: str) -> NetworkInterface:
    return NoShutdownNetworkInterface(get_appliance(node_name)).no_shutdown(svi)


def get_appliance(node_name: str) -> Appliance:
    repository = NodeRepositoryFactory.get_repository(repo_type)
    node: NodeWithCredentials = repository.retrieve_with_credentials(node_name)
    return ApplianceFactory.get_appliance(node)
