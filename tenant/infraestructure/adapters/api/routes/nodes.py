from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from tenant.application.usecases.node.create_node import CreateNode
from tenant.application.usecases.node.delete_node import DeleteNode
from tenant.application.usecases.node.read_all_nodes import ReadAllNodes
from tenant.application.usecases.node.read_node import ReadNode
from tenant.application.usecases.node.update_node import UpdateNode
from tenant.domain.schemas.node.deleted_node_response import DeletedNodeResponse
from tenant.domain.schemas.node.existing_node import ExistingNode
from tenant.domain.schemas.node.new_node import NewNode
from tenant.domain.ports.nodes.interface_delete_node import IDeleteNode
from tenant.domain.ports.nodes.interface_update_node import IUpdateNode
from tenant.domain.ports.nodes.interface_read_all_nodes import IReadAllNodes
from tenant.domain.ports.nodes.interface_read_node import IReadNode
from tenant.domain.ports.nodes.interface_create_node import ICreateNode
from tenant.domain.models.repository_type import RepositoryType
from tenant.domain.models.role_checker import RoleChecker
from tenant.domain.models.role import Role
from tenant.domain.schemas.node.node import Node
from tenant.domain.schemas.node.node_response import NodeResponse
from tenant.infraestructure.adapters.appliances.appliance_factory import ApplianceFactory
from tenant.infraestructure.adapters.repositories.factories.compatible_node_repository_factory import \
    CompatibleNodeRepositoryFactory
from tenant.infraestructure.adapters.repositories.factories.node_respository_factory import NodeRepositoryFactory

nodes_router = APIRouter(prefix="/api/v1/nodes", tags=["Nodes"])

REPOSITORY: RepositoryType = RepositoryType.mongo_db_user

repo_node = NodeRepositoryFactory.get_repository(RepositoryType.mongo_db_user)
repo_compatible_node = CompatibleNodeRepositoryFactory.get_repository(RepositoryType.mongo_db_user)

allow_access_write = RoleChecker([Role.admin, Role.editor])
allow_access_read = RoleChecker([Role.admin, Role.editor, Role.viewer])


@nodes_router.get("/", response_model=list[NodeResponse], dependencies=[Depends(allow_access_read)])
async def read_all_nodes() -> list[NodeResponse]:
    nodes: IReadAllNodes = ReadAllNodes(repo_node)
    return nodes.retrieve_all()


@nodes_router.get("/{name}", response_model=NodeResponse, dependencies=[Depends(allow_access_read)])
async def read_node(name: str) -> NodeResponse:
    if not await _node_exist(name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ERROR: Node NOT found", )

    node: IReadNode = (ReadNode(repo_node))
    return node.retrieve(name)


@nodes_router.post("/", status_code=201, dependencies=[Depends(allow_access_write)])
async def create_new_node(node: NewNode) -> NodeResponse:
    if await _node_exist(node.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ERROR: Node exists")

    create_node: ICreateNode = CreateNode(repo_node)
    return create_node.save(node)


@nodes_router.patch("/", status_code=201, response_model=NodeResponse, dependencies=[Depends(allow_access_write)])
async def update_node(existing_node: ExistingNode) -> NodeResponse:
    if not await _node_exist(existing_node.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ERROR: Node NOT found, can't be updated")

    node: IUpdateNode = UpdateNode(repo_node)
    return node.update(existing_node)


@nodes_router.delete("/{username}", status_code=202, dependencies=[Depends(allow_access_write)])
async def delete_node_by_name(node_name: str) -> DeletedNodeResponse:
    if not await _node_exist(node_name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ERROR: Node NOT found, can't be deleted")

    node: IDeleteNode = DeleteNode(repo_node)
    return node.delete(node_name)


@nodes_router.get("/status/{name}", status_code=200, dependencies=[Depends(allow_access_read)])
async def get_node_status(name: str) -> dict:
    if not await _node_exist(name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="ERROR: Node NOT found. Please, check if exists.")
    node = await read_node(name)
    appliance = ApplianceFactory.get_appliance(node)
    if appliance.service_status():
        return {"status": "OK", "message": f"appliance {name} is reachable"}
    else:
        return {"status": "KO", "message": f"appliance {name} NOT reachable. Please, check connection"}


async def _node_exist(node_name: str) -> bool:
    node: IReadNode = (ReadNode(repo_node))
    response: Node = node.retrieve(node_name)
    if response != {}:
        return True

    return False
