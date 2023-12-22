from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.node.existing_node import ExistingNode
from tenant.domain.schemas.node.node_response import NodeResponse


class IUpdateNode(metaclass=ABCMeta):

    @abstractmethod
    def update(self, user: ExistingNode) -> NodeResponse:
        ...
