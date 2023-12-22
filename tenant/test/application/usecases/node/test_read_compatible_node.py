from unittest.mock import Mock
from tenant.domain.schemas.node.compatible_node_search import CompatibleNodeSearch
from tenant.application.usecases.node.read_compatible_node import ReadCompatibleNode
from tenant.infraestructure.gateways.interface_compatible_node_repository import ICompatibleNodeRepository


def test_compatible_nodes_when_valid_search_provided():
    mock_repository = Mock(spec=ICompatibleNodeRepository)
    mock_repository.retrieve.return_value = [CompatibleNodeSearch()]

    usecase = ReadCompatibleNode(mock_repository)
    result = usecase.retrieve(CompatibleNodeSearch())

    assert len(result) > 0


def test_empty_when_no_matching_search_provided():
    mock_repository = Mock(spec=ICompatibleNodeRepository)
    mock_repository.retrieve.return_value = []

    usecase = ReadCompatibleNode(mock_repository)
    result = usecase.retrieve(CompatibleNodeSearch())

    assert len(result) == 0


def test_exception_when_invalid_search_provided():
    mock_repository = Mock(spec=ICompatibleNodeRepository)
    mock_repository.retrieve.side_effect = Exception

    usecase = ReadCompatibleNode(mock_repository)

    try:
        usecase.retrieve(CompatibleNodeSearch())
        assert False
    except Exception:
        assert True
