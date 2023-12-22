import pytest
from unittest.mock import Mock, patch
from tenant.infraestructure.adapters.repositories.atlas_mongo_db_compatible_repository import \
    AtlasMongoDBCompatibleNodeRepository
from tenant.domain.schemas.node.compatible_node_search import CompatibleNodeSearch


class TestAtlasMongoDBCompatibleNodeRepository:

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_compatible_repository.MongoClient')
    def test_should_return_compatible_nodes_when_retrieve_is_called_with_valid_search(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.find.return_value = [
            {"vendor": "Vendor1", "model": "Model1", "technology": "Tech1", "softwareVersion": "1.0"}]
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBCompatibleNodeRepository()
        result = repository.retrieve(CompatibleNodeSearch(vendor="Vendor1"))

        assert len(result) > 0
        assert isinstance(result[0], dict)
        assert result[0]["vendor"] == "Vendor1"

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_compatible_repository.MongoClient')
    def test_should_return_empty_dict_when_retrieve_is_called_with_no_matching_search(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.find.return_value = []
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBCompatibleNodeRepository()
        result = repository.retrieve(CompatibleNodeSearch(vendor="Vendor2"))

        assert len(result) == 0

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_compatible_repository.MongoClient')
    def test_should_return_all_compatible_nodes_when_retrieve_all_is_called(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.find.return_value = [
            {"vendor": "Vendor1", "model": "Model1", "technology": "Tech1", "softwareVersion": "1.0"},
            {"vendor": "Vendor2", "model": "Model2", "technology": "Tech2", "softwareVersion": "2.0"}]
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBCompatibleNodeRepository()
        result = repository.retrieve_all()

        assert len(result) == 2
        assert isinstance(result[0], dict)
        assert result[0]["vendor"] == "Vendor1"
        assert isinstance(result[1], dict)
        assert result[1]["vendor"] == "Vendor2"
