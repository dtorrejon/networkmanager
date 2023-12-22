from tenant.domain.schemas.node.compatible_node_search import CompatibleNodeSearch
from tenant.domain.ports.nodes.interface_read_compatible_node import IReadCompatibleNode
from tenant.infraestructure.gateways.interface_compatible_node_repository import ICompatibleNodeRepository


class ReadCompatibleNode(IReadCompatibleNode):

    def __init__(self, compatible_node_repository: ICompatibleNodeRepository):
        self.compatible_node_repository = compatible_node_repository

    def retrieve(self, compatible_node: CompatibleNodeSearch) -> list[CompatibleNodeSearch]:
        return self.compatible_node_repository.retrieve(compatible_node)
