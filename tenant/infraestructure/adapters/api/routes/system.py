from fastapi import APIRouter, Depends

from tenant.application.usecases.appliance.system.launch_restart import LaunchRestart
from tenant.application.usecases.appliance.system.set_hostname import SetHostname
from tenant.domain.schemas.appliances.system.hostname import Hostname
from tenant.domain.schemas.appliances.system.restart import Restart
from tenant.domain.schemas.node.existing_node import ExistingNode
from tenant.domain.models.role import Role
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.domain.ports.appliances.system.interface_launch_restart import ILaunchRestart
from tenant.domain.ports.appliances.system.interface_set_hostname import ISetHostname
from tenant.domain.models.repository_type import RepositoryType
from tenant.domain.models.role_checker import RoleChecker
from tenant.infraestructure.adapters.appliances.appliance_factory import ApplianceFactory
from tenant.infraestructure.adapters.repositories.factories.node_respository_factory import NodeRepositoryFactory

system_router = APIRouter(prefix="/api/v1/system", tags=["System"])

repo_node = NodeRepositoryFactory.get_repository(RepositoryType.mongo_db_user)

allow_access_read = RoleChecker([Role.admin, Role.editor])


@system_router.get("/reboot/{node_name}", response_model=Restart, dependencies=[Depends(allow_access_read)])
async def reboot(node_name: str):
    node: NodeWithCredentials = repo_node.retrieve_with_credentials(node_name)
    appliance = ApplianceFactory.get_appliance(node)
    launch_restart: ILaunchRestart = LaunchRestart(appliance)
    return launch_restart.restart()

@system_router.put("/hostname/{node_name}/{new_node_name}", response_model=Hostname, dependencies=[Depends(allow_access_read)])
async def hostname(node_name: str, new_node_name: str):
    node: NodeWithCredentials = repo_node.retrieve_with_credentials(node_name)
    appliance = ApplianceFactory.get_appliance(node)
    update_response = repo_node.update(ExistingNode(name=node_name, newName=new_node_name))
    set_hostname: ISetHostname = SetHostname(appliance)
    return set_hostname.set_hostname(new_node_name)
