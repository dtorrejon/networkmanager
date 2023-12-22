from tenant.application.password_crypt import PasswordCrypt
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.domain.ports.nodes.interface_read_node_with_credentials import IReadNodeWithCredentials
from tenant.infraestructure.gateways.interface_node_repository import INodeRepository


class ReadNodeWithCredentials(IReadNodeWithCredentials):

    def __init__(self, node_repository: INodeRepository):
        self.node_repository = node_repository

    def retrieve(self, node_name: str) -> NodeWithCredentials:
        response = self.node_repository.retrieve_with_credentials(node_name)
        pc = PasswordCrypt()
        response.password = pc.decode_password(response.password)
        return response
