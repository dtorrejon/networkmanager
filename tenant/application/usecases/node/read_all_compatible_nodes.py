from tenant.domain.schemas.node.compatible_node_search import CompatibleNodeSearch
from tenant.domain.ports.nodes.interfaces_read_all_compatible_nodes import IReadAllCompatibleNodes
from tenant.infraestructure.gateways.interface_compatible_node_repository import ICompatibleNodeRepository


class ReadAllCompatibleNodes(IReadAllCompatibleNodes):

    def __init__(self, compatible_node_repository: ICompatibleNodeRepository):
        self.compatible_node_repository = compatible_node_repository

    def retrieve_all(self) -> list[CompatibleNodeSearch]:
        return self.compatible_node_repository.retrieve_all()
