from fastapi import APIRouter, Depends

from tenant.application.usecases.appliance.commands.send_command import SendCommand
from tenant.application.usecases.appliance.commands.send_script import SendScript
from tenant.domain.schemas.appliances.commands.command import Command
from tenant.domain.schemas.appliances.commands.script import Script
from tenant.domain.models.repository_type import RepositoryType
from tenant.domain.models.role import Role
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.domain.models.role_checker import RoleChecker
from tenant.infraestructure.adapters.appliances.appliance_factory import ApplianceFactory
from tenant.infraestructure.adapters.repositories.factories.node_respository_factory import NodeRepositoryFactory
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance

commands_router = APIRouter(prefix="/api/v1/command", tags=["Commands"])

repo_type = RepositoryType.mongo_db_user

allow_access_edit = RoleChecker([Role.admin, Role.editor])


@commands_router.post("/{node_name}", response_model=Command,
                      dependencies=[Depends(allow_access_edit)])
async def send_command(node_name: str, command: str) -> Command:
    return SendCommand(get_appliance(node_name)).send_command(command)


@commands_router.post("/script/{node_name}", response_model=list[Command],
                      dependencies=[Depends(allow_access_edit)])
async def send_script(node_name: str, script: Script):
    return SendScript(get_appliance(node_name)).send_script(script)


def get_appliance(node_name: str) -> Appliance:
    repository = NodeRepositoryFactory.get_repository(repo_type)
    node: NodeWithCredentials = repository.retrieve_with_credentials(node_name)
    return ApplianceFactory.get_appliance(node)
