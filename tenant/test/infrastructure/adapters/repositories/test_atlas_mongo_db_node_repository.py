import pytest
from unittest.mock import Mock, patch
from tenant.infraestructure.adapters.repositories.atlas_mongo_db_node_repository import AtlasMongoDBNodeRepository
from tenant.domain.schemas.node.node import Node
from tenant.domain.schemas.node.existing_node import ExistingNode


class TestAtlasMongoDBNodeRepository:

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_node_repository.MongoClient')
    def test_should_return_node_response_when_save_is_called_with_valid_node(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.insert_one.return_value = True
        mock_collection.find_one.return_value = {"name": "Node Name", "vendor": "Vendor", "technology": "Tech",
                                                 "model": "Model", "softwareVersion": "1.0", "ipAddress": "192.168.1.1",
                                                 "protocol": "ssh", "port": 1234}
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBNodeRepository()
        result = repository.save(
            Node(name="Node Name", vendor="Vendor", technology="Tech", model="Model", softwareVersion="1.0",
                 ipAddress="192.168.1.1", protocol="ssh", port=1234))

        assert result.name == "Node Name"
        assert result.vendor == "Vendor"
        assert result.technology == "Tech"
        assert result.model == "Model"
        assert result.softwareVersion == "1.0"
        assert result.ipAddress == "192.168.1.1"
        assert result.protocol == "ssh"
        assert result.port == 1234

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_node_repository.MongoClient')
    def test_should_return_empty_dict_when_retrieve_is_called_with_no_matching_node_name(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.find_one.return_value = None
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBNodeRepository()
        result = repository.retrieve("Nonexistent Node Name")

        assert result == {}

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_node_repository.MongoClient')
    def test_should_return_all_node_responses_when_retrieve_all_is_called(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.find.return_value = [
            {"name": "Node Name 1", "vendor": "Vendor 1", "technology": "Tech 1", "model": "Model 1",
             "softwareVersion": "1.0", "ipAddress": "192.168.1.1", "protocol": "telnet", "port": 23},
            {"name": "Node Name 2", "vendor": "Vendor 2", "technology": "Tech 2", "model": "Model 2",
             "softwareVersion": "2.0", "ipAddress": "192.168.2.2", "protocol": "ssh", "port": 22}]
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBNodeRepository()
        result = repository.retrieve_all()
        assert len(result) == 2
        assert result[0]["name"] == "Node Name 1"
        assert result[1]["name"] == "Node Name 2"

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_node_repository.MongoClient')
    def test_should_return_updated_node_response_when_update_is_called_with_valid_existing_node(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.find_one.return_value = {"name": "Updated Node Name", "vendor": "Updated Vendor",
                                                 "technology": "Updated Tech", "model": "Updated Model",
                                                 "softwareVersion": "2.0", "ipAddress": "192.168.2.2",
                                                 "protocol": "telnet", "port": 2345}
        mock_collection.find_one_and_update.return_value = True
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBNodeRepository()
        result = repository.update(ExistingNode(name="Node Name", newName="Updated Node Name", vendor="Updated Vendor",
                                                technology="Updated Tech", model="Updated Model", softwareVersion="2.0",
                                                ipAddress="192.168.2.2", protocol="telnet", port=2345))

        assert result.name == "Updated Node Name"
        assert result.vendor == "Updated Vendor"
        assert result.technology == "Updated Tech"
        assert result.model == "Updated Model"
        assert result.softwareVersion == "2.0"
        assert result.ipAddress == "192.168.2.2"
        assert result.protocol == "telnet"
        assert result.port == 2345

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_node_repository.MongoClient')
    def test_should_return_empty_dict_when_update_is_called_with_no_matching_node_name(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.find_one.return_value = None
        mock_collection.find_one_and_update.return_value = None
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBNodeRepository()
        result = repository.update(
            ExistingNode(name="Nonexistent Node Name", newName="Updated Node Name", vendor="Updated Vendor",
                         technology="Updated Tech", model="Updated Model", softwareVersion="2.0",
                         ipAddress="192.168.2.2", protocol="ssh", port=2345))

        assert result == {}

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_node_repository.MongoClient')
    def test_should_return_deleted_node_response_when_delete_is_called_with_valid_node_name(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.delete_one.return_value = True
        mock_collection.find_one.return_value = None
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBNodeRepository()
        result = repository.delete("Node Name")

        assert result.status == "ok"
        assert result.message == "Node Node Name has been deleted"

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_node_repository.MongoClient')
    def test_should_return_deleted_node_response_with_error_message_when_delete_is_called_with_invalid_node_name(
            mock_mongo_client):
        mock_collection = Mock()
        mock_collection.delete_one.return_value = False
        mock_collection.find_one.return_value = {"name": "Node Name", "vendor": "Vendor", "technology": "Tech",
                                                 "model": "Model", "softwareVersion": "1.0", "ipAddress": "192.168.1.1",
                                                 "protocol": "ssh", "port": 1234}
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBNodeRepository()
        result = repository.delete("Invalid Node Name")

        assert result.status == "nok"
        assert result.message == "Node Invalid Node Name couldn't be deleted"
