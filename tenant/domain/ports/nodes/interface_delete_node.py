from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.node.deleted_node_response import DeletedNodeResponse


class IDeleteNode(metaclass=ABCMeta):

    @abstractmethod
    def delete(self, node_name: str) -> DeletedNodeResponse:
        ...
