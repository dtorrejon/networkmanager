from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.node.node_connection_status import NodeConnectionStatus


class IStatusNode(metaclass=ABCMeta):
    @abstractmethod
    def status(self, node_name: str) -> NodeConnectionStatus:
        ...
