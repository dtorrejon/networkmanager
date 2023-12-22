from unittest.mock import Mock
from tenant.application.usecases.node.create_node import CreateNode
from tenant.domain.schemas.node.new_node import NewNode
from tenant.domain.schemas.node.node import Node


def test_create_node_with_valid_data():
    new_node = NewNode(**{
        "name": "switch-1",
        "vendor": "cisco",
        "technology": "switch3",
        "model": "2960",
        "softwareVersion": "c2960-lanlitek9-mz.150-2.SE11",
        "ipAddress": "192.168.1.1",
        "protocol": "ssh",
        "username": "testuser",
        "password": "password123"
    })
    node_response = Node(**{
        "name": "switch-1",
        "vendor": "cisco",
        "technology": "switch3",
        "model": "2960",
        "softwareVersion": "c2960-lanlitek9-mz.150-2.SE11",
        "ipAddress": "192.168.1.1",
        "protocol": "ssh",
        "port": 22})
    mock_node_repository = Mock()
    mock_node_repository.save.return_value = node_response
    create_node = CreateNode(mock_node_repository)
    assert create_node.save(new_node) == node_response


def test_create_node_with_existing_name():
    mock_node_repository = Mock()
    mock_node_repository.save.side_effect = Exception("Node already exists")
    create_node = CreateNode(mock_node_repository)
    new_node = NewNode(**{
        "name": "switch-1",
        "vendor": "cisco",
        "technology": "switch3",
        "model": "2960",
        "softwareVersion": "c2960-lanlitek9-mz.150-2.SE11",
        "ipAddress": "192.168.1.1",
        "protocol": "ssh",
        "username": "testuser",
        "password": "password123"
    })
    try:
        create_node.save(new_node)
    except Exception as e:
        assert str(e) == "Node already exists"

def test_create_node_with_empty_name():
    mock_node_repository = Mock()
    mock_node_repository.save.side_effect = Exception("Node name cannot be empty")
    try:
        NewNode(**{
            "name": "",
            "vendor": "cisco",
            "technology": "switch3",
            "model": "2960",
            "softwareVersion": "c2960-lanlitek9-mz.150-2.SE11",
            "ipAddress": "192.168.1.1",
            "protocol": "ssh",
            "username": "testuser",
            "password": "password123"
        })
    except Exception as e:
        assert str(e) == "Node name cannot be empty"


def test_create_node_with_empty_password():
    mock_node_repository = Mock()
    mock_node_repository.save.side_effect = Exception("Node name cannot be empty")
    try:
        NewNode(**{
            "name": "sw01",
            "vendor": "cisco",
            "technology": "switch3",
            "model": "2960",
            "softwareVersion": "c2960-lanlitek9-mz.150-2.SE11",
            "ipAddress": "192.168.1.1",
            "protocol": "ssh",
            "username": "testuser",
            "password": ""
        })

    except Exception as e:
        assert str(e) == "Password cannot be empty"




