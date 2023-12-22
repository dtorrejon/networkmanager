from tenant.domain.ports.nodes.interface_read_node import IReadNode
from tenant.domain.schemas.node.node_response import NodeResponse
from tenant.infraestructure.gateways.interface_node_repository import INodeRepository


class ReadNode(IReadNode):

    def __init__(self, node_repository: INodeRepository):
        self.node_repository = node_repository

    def retrieve(self, node_name: str) -> NodeResponse:
        return self.node_repository.retrieve(node_name)


