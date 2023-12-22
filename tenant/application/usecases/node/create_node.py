from tenant.application.password_crypt import PasswordCrypt
from tenant.domain.schemas.node.new_node import NewNode
from tenant.domain.ports.nodes.interface_create_node import ICreateNode
from tenant.domain.schemas.node.node import Node
from tenant.infraestructure.gateways.interface_node_repository import INodeRepository


class CreateNode(ICreateNode):

    def __init__(self, node_repository: INodeRepository):
        self.node_repository = node_repository

    def save(self, node: NewNode) -> Node:
        node.password = PasswordCrypt().encode_password(node.password)
        return self.node_repository.save(node)
