from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials


class IReadNodeWithCredentials(metaclass=ABCMeta):

    @abstractmethod
    def retrieve(self, node_name: str) -> NodeWithCredentials:
        ...
