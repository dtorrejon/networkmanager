from abc import ABCMeta, abstractmethod
from tenant.domain.schemas.node.compatible_node_search import CompatibleNodeSearch


class ICompatibleNodeRepository(metaclass=ABCMeta):

    @abstractmethod
    def retrieve(self, compatible_node: CompatibleNodeSearch) -> list[CompatibleNodeSearch]:
        ...

    @abstractmethod
    def retrieve_all(self) -> list[CompatibleNodeSearch]:
        ...
