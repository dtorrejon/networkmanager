from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.node.compatible_node_search import CompatibleNodeSearch


class IReadCompatibleNode(metaclass=ABCMeta):

    @abstractmethod
    def retrieve(self, compatible_node: CompatibleNodeSearch) -> list[CompatibleNodeSearch]:
        ...
