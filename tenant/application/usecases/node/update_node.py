
from tenant.application.password_crypt import PasswordCrypt
from tenant.domain.schemas.node.existing_node import ExistingNode
from tenant.domain.ports.nodes.interface_update_node import IUpdateNode
from tenant.domain.schemas.node.node_response import NodeResponse
from tenant.infraestructure.gateways.interface_node_repository import INodeRepository


class UpdateNode(IUpdateNode):

    def __init__(self, node_repository: INodeRepository):
        self.user_repository = node_repository

    def update(self, node: ExistingNode) -> NodeResponse:
        if node.password != "":
            node.password = PasswordCrypt().encode_password(node.password)
        return self.user_repository.update(node)
