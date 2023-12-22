import pytest
from unittest.mock import Mock
from tenant.domain.schemas.node.node_response import NodeResponse
from tenant.application.usecases.node.read_all_nodes import ReadAllNodes


def test_nodes_retrieval_with_data():
    mock_repository = Mock()
    mock_repository.retrieve_all.return_value = [NodeResponse(**{
        "name": "switch01",
        "technology": "switchl3",
        "vendor": "cisco",
        "model": "ioul2",
        "softwareVersion": "15.5(2)T",
        "ipAddress": "192.168.20.10",
        "protocol": "telnet",
        "port": 23
    }), NodeResponse(**{
        "name": "hua01",
        "technology": "switchl3",
        "vendor": "huawei",
        "model": "s5730",
        "softwareVersion": "15",
        "ipAddress": "192.168.10.10",
        "protocol": "ssh",
        "port": 22
    })]
    use_case = ReadAllNodes(mock_repository)
    assert len(use_case.retrieve_all()) == 2


def test_nodes_retrieval_with_no_data():
    mock_repository = Mock()
    mock_repository.retrieve_all.return_value = []
    use_case = ReadAllNodes(mock_repository)
    assert len(use_case.retrieve_all()) == 0
