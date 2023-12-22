from tenant.domain.schemas.node.deleted_node_response import DeletedNodeResponse
from tenant.domain.ports.nodes.interface_delete_node import IDeleteNode
from tenant.infraestructure.gateways.interface_node_repository import INodeRepository


class DeleteNode(IDeleteNode):

    def __init__(self, node_repository: INodeRepository):
        self.node_repository = node_repository

    def delete(self, node_name: str) -> DeletedNodeResponse:
        return self.node_repository.delete(node_name)
