from typing import Union, Optional

from fastapi import APIRouter, Depends

from tenant.application.usecases.appliance.vlan.display_vlan_brief import DisplayVlanBrief
from tenant.application.usecases.appliance.vlan.display_vlan_trunk import DisplayVlanTrunk
from tenant.application.usecases.appliance.vlan.remove_vlan import RemoveVlan
from tenant.application.usecases.appliance.vlan.set_vlan_access import SetVlanAccess
from tenant.application.usecases.appliance.vlan.set_vlan_native import SetVlanNative
from tenant.application.usecases.appliance.vlan.set_vlan_trunk import SetVlanTrunk
from tenant.domain.schemas.appliances.vlans.vlan_brief import VlanBrief
from tenant.domain.schemas.appliances.vlans.vlan_resume import VlanResume
from tenant.domain.schemas.appliances.vlans.vlan_trunk import VlanTrunk
from tenant.domain.models.repository_type import RepositoryType
from tenant.domain.models.role import Role
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.domain.models.role_checker import RoleChecker
from tenant.infraestructure.adapters.appliances.appliance_factory import ApplianceFactory
from tenant.infraestructure.adapters.repositories.factories.node_respository_factory import NodeRepositoryFactory
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance

vlan_router = APIRouter(prefix="/api/v1/vlan", tags=["Vlans management"])

repo_type = RepositoryType.mongo_db_user

allow_access_read = RoleChecker([Role.admin, Role.editor, Role.viewer])
allow_access_edit = RoleChecker([Role.admin, Role.editor])


@vlan_router.get("/brief/{node_name}", response_model=list[VlanBrief],
                 dependencies=[Depends(allow_access_read)])
async def display_vlan_brief(node_name: str) -> list[VlanBrief]:
    return DisplayVlanBrief(get_appliance(node_name)).display_brief()


@vlan_router.get("/vlan/trunk/{node_name}", response_model=list[VlanTrunk], dependencies=[Depends(allow_access_read)])
async def display_vlan_trunk(node_name: str) -> list[VlanTrunk]:
    return DisplayVlanTrunk(get_appliance(node_name)).display()


@vlan_router.put("/access/{node_name}", response_model=list[VlanBrief], dependencies=[Depends(allow_access_edit)])
async def set_vlan_access(node_name: str, interface: str, vlan_id: int, bridge: Optional[str] = None) -> list[VlanBrief]:
    return SetVlanAccess(get_appliance(node_name)).set_vlan_access(interface, vlan_id, bridge)


@vlan_router.put("/trunk/{node_name}", response_model=list[VlanTrunk],
                 dependencies=[Depends(allow_access_edit)])
async def set_vlan_trunk(node_name: str, interface: str, vlan_id: list[int], bridge: Optional[str] = None) -> list[VlanTrunk]:
    return SetVlanTrunk(get_appliance(node_name)).set_vlan_trunk(interface, vlan_id, bridge)


@vlan_router.put("/native/{node_name}", response_model=list[VlanTrunk],
                 dependencies=[Depends(allow_access_edit)])
async def set_vlan_native(node_name: str, interface: str, vlan_id: int, bridge: Optional[str] = None) -> list[VlanTrunk]:
    return SetVlanNative(get_appliance(node_name)).set_vlan_native(interface, vlan_id, bridge)


@vlan_router.delete("/{node_name}", response_model=VlanResume,
                    dependencies=[Depends(allow_access_edit)])
async def remove_vlan(node_name: str, vlan_id: Union[int, str], interface: str) -> VlanResume:
    return RemoveVlan(get_appliance(node_name)).remove_vlan(interface, vlan_id)


def get_appliance(node_name: str) -> Appliance:
    repository = NodeRepositoryFactory.get_repository(repo_type)
    node: NodeWithCredentials = repository.retrieve_with_credentials(node_name)
    return ApplianceFactory.get_appliance(node)
