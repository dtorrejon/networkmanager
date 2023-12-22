from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.node.compatible_node_search import CompatibleNodeSearch


class IReadAllCompatibleNodes(metaclass=ABCMeta):

    @abstractmethod
    def retrieve_all(self) -> list[CompatibleNodeSearch]:
        ...
