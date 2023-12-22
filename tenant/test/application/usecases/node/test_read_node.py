from unittest.mock import Mock
from tenant.domain.schemas.node.node_response import NodeResponse
from tenant.application.usecases.node.read_node import ReadNode
from tenant.infraestructure.gateways.interface_node_repository import INodeRepository

def test_retrieve_is_called_with_valid_node_name():
    mock_repository = Mock(spec=INodeRepository)
    mock_repository.retrieve.return_value = NodeResponse(**{
        "name": "hua01",
        "technology": "switchl3",
        "vendor": "huawei",
        "model": "s5730",
        "softwareVersion": "15",
        "ipAddress": "192.168.10.10",
        "protocol": "ssh",
        "port": 22
    })

    usecase = ReadNode(mock_repository)
    result = usecase.retrieve("valid_node_name")

    assert isinstance(result, NodeResponse)

def test_retrieve_is_called_with_invalid_node_name():
    mock_repository = Mock(spec=INodeRepository)
    mock_repository.retrieve.side_effect = Exception

    usecase = ReadNode(mock_repository)

    try:
        usecase.retrieve("invalid_node_name")
        assert False
    except Exception:
        assert True

def test_retrieve_is_called_with_no_node_name():
    mock_repository = Mock(spec=INodeRepository)
    mock_repository.retrieve.return_value = None

    usecase = ReadNode(mock_repository)
    result = usecase.retrieve(None)

    assert result is None
