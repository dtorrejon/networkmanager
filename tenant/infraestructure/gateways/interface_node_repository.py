from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.node.deleted_node_response import DeletedNodeResponse
from tenant.domain.schemas.node.existing_node import ExistingNode
from tenant.domain.schemas.node.new_node import NewNode
from tenant.domain.schemas.node.node_response import NodeResponse
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials


class INodeRepository(metaclass=ABCMeta):

    @abstractmethod
    def save(self, node: NewNode) -> NodeResponse:
        ...

    @abstractmethod
    def retrieve(self, node_name: str) -> NodeResponse:
        ...

    @abstractmethod
    def retrieve_with_credentials(self, node_name: str) -> NodeWithCredentials:
        ...

    @abstractmethod
    def retrieve_all(self) -> list[NodeResponse]:
        ...

    @abstractmethod
    def update(self, node: ExistingNode) -> NodeResponse:
        ...

    @abstractmethod
    def delete(self, node_name: str) -> DeletedNodeResponse:
        ...
