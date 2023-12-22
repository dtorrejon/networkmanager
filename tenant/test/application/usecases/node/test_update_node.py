
from unittest.mock import Mock
from tenant.domain.schemas.node.existing_node import ExistingNode
from tenant.application.usecases.node.update_node import UpdateNode
from tenant.infraestructure.gateways.interface_node_repository import INodeRepository

def test_password_when_update_is_called_with_password():
    mock_repository = Mock(spec=INodeRepository)
    mock_node = ExistingNode()
    mock_node.password = "plain_password"
    mock_repository.update.return_value = mock_node

    usecase = UpdateNode(mock_repository)
    result = usecase.update(mock_node)

    assert isinstance(result, ExistingNode)
    assert result.password != "plain_password"

def test_not_change_password_when_update_is_called_with_empty_password():
    mock_repository = Mock(spec=INodeRepository)
    mock_node = ExistingNode()
    mock_node.password = ""
    mock_repository.update.return_value = mock_node

    usecase = UpdateNode(mock_repository)
    result = usecase.update(mock_node)

    assert isinstance(result, ExistingNode)
