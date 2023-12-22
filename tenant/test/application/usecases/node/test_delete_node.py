from unittest.mock import Mock
import pytest
from tenant.application.usecases.node.delete_node import DeleteNode
from tenant.domain.schemas.node.deleted_node_response import DeletedNodeResponse
from tenant.infraestructure.gateways.interface_node_repository import INodeRepository


def test_delete_node_successfully():
    node_repository = Mock()
    node_repository.delete.return_value = DeletedNodeResponse(
        **{"status": "ok", "message": "Node deleted successfully"})
    delete_node = DeleteNode(node_repository)
    response = delete_node.delete("Node-1")
    assert response.model_dump() == {"status": "ok", "message": "Node deleted successfully"}


def test_delete_node_with_nonexistent_name():
    node_repository = Mock()
    node_repository.delete.return_value = DeletedNodeResponse(
        **{"status": "nok", "message": "Node not found"})
    delete_node = DeleteNode(node_repository)
    response = delete_node.delete("Nonexistent-Node")
    assert response.model_dump() == {"status": "nok", "message": "Node not found"}
