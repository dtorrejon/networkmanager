from typing import Optional

from fastapi import APIRouter, Depends
from tenant.application.usecases.node.read_compatible_node import ReadCompatibleNode
from tenant.domain.schemas.node.compatible_node_search import CompatibleNodeSearch
from tenant.domain.ports.nodes.interface_read_compatible_node import IReadCompatibleNode
from tenant.domain.models.repository_type import RepositoryType
from tenant.domain.models.role_checker import RoleChecker
from tenant.domain.models.role import Role
from tenant.infraestructure.adapters.repositories.factories.compatible_node_repository_factory import \
    CompatibleNodeRepositoryFactory

compatible_nodes_router = APIRouter(prefix="/api/v1/nodes/compatibility", tags=["Nodes Compatibility"])

repository = CompatibleNodeRepositoryFactory.get_repository(RepositoryType.mongo_db_user)

allow_access_read = RoleChecker([Role.admin, Role.editor, Role.viewer])

"""
@compatible_nodes_router.get("/", dependencies=[Depends(allow_access_read)])
async def read_all_compatible_nodes() -> dict:
    compatible_nodes: IReadAllCompatibleNodes = ReadAllCompatibleNodes(repository)
    return compatible_nodes.retrieve_all()
"""


@compatible_nodes_router.get("/",
                             dependencies=[Depends(allow_access_read)])
async def read_compatible_nodes(technology: Optional[str] = None, vendor: Optional[str] = None,
                                model: Optional[str] = None, software_version: Optional[str] = None) -> dict:
    compatible_node = CompatibleNodeSearch(technology=technology, vendor=vendor, model=model,
                                           software_version=software_version)
    node: IReadCompatibleNode = ReadCompatibleNode(repository)
    return node.retrieve(compatible_node)
