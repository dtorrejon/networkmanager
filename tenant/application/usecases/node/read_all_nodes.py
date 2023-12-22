from tenant.domain.ports.nodes.interface_read_all_nodes import IReadAllNodes
from tenant.domain.schemas.node.node_response import NodeResponse
from tenant.infraestructure.gateways.interface_node_repository import INodeRepository


class ReadAllNodes(IReadAllNodes):

    def __init__(self, node_repository: INodeRepository):
        self.node_repository = node_repository

    def retrieve_all(self) -> list[NodeResponse]:
        return self.node_repository.retrieve_all()