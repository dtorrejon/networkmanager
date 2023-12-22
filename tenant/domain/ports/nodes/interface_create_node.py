from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.node.new_node import NewNode
from tenant.domain.schemas.node.node_response import NodeResponse


class ICreateNode(metaclass=ABCMeta):

    @abstractmethod
    def save(self, node: NewNode) -> NodeResponse:
        ...
