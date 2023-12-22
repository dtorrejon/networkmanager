from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.node.node_response import NodeResponse


class IReadAllNodes(metaclass=ABCMeta):

    @abstractmethod
    def retrieve_all(self) -> list[NodeResponse]:
        ...
