from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.node.node_response import NodeResponse


class IReadNode(metaclass=ABCMeta):

    @abstractmethod
    def retrieve(self, node_name: str) -> NodeResponse:
        ...
