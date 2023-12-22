import pytest
from unittest.mock import Mock
from tenant.domain.schemas.node.compatible_node_search import CompatibleNodeSearch
from tenant.application.usecases.node.read_all_compatible_nodes import ReadAllCompatibleNodes

def test_compatible_nodes_retrieval_with_data():
    # Mocking the repository
    mock_repository = Mock()
    mock_repository.retrieve_all.return_value = [CompatibleNodeSearch(), CompatibleNodeSearch()]

    # Creating the use case with the mocked repository
    use_case = ReadAllCompatibleNodes(mock_repository)

    # Asserting the use case retrieves the expected data
    assert len(use_case.retrieve_all()) == 2

def test_compatible_nodes_retrieval_with_no_data():
    # Mocking the repository
    mock_repository = Mock()
    mock_repository.retrieve_all.return_value = []

    # Creating the use case with the mocked repository
    use_case = ReadAllCompatibleNodes(mock_repository)

    # Asserting the use case retrieves an empty list when no data is available
    assert len(use_case.retrieve_all()) == 0
