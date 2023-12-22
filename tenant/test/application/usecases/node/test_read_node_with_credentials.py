from unittest.mock import Mock

from tenant.application.password_crypt import PasswordCrypt
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.application.usecases.node.read_node_with_credentials import ReadNodeWithCredentials
from tenant.infraestructure.gateways.interface_node_repository import INodeRepository


def test_node_with_decoded_password_when_retrieve_is_called_with_valid_node_name_and_encoded_password():
    mock_repository = Mock(spec=INodeRepository)
    pc = PasswordCrypt()
    mock_node = NodeWithCredentials(**{
        "name": "hua01",
        "technology": "switchl3",
        "vendor": "huawei",
        "model": "s5730",
        "softwareVersion": "15",
        "ipAddress": "192.168.10.10",
        "protocol": "ssh",
        "port": 22,
        "username": "admin",
        "password": f"{pc.encode_password('encoded_password')}"
    })
    mock_repository.retrieve_with_credentials.return_value = mock_node

    usecase = ReadNodeWithCredentials(mock_repository)
    result = usecase.retrieve("hua01")

    assert isinstance(result, NodeWithCredentials)
    assert result.password == 'encoded_password'


def test_retrieve_is_called_with_invalid_node_name():
    mock_repository = Mock(spec=INodeRepository)
    mock_repository.retrieve_with_credentials.side_effect = Exception

    usecase = ReadNodeWithCredentials(mock_repository)

    try:
        usecase.retrieve("invalid_node_name")
        assert False
    except Exception:
        assert True


