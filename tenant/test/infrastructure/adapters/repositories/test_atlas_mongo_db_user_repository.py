import pytest
from unittest.mock import Mock, patch
from tenant.infraestructure.adapters.repositories.atlas_mongo_db_user_repository import AtlasMongoDBUserRepository
from tenant.domain.schemas.users.new_user import NewUser
from tenant.domain.schemas.users.updating_user import UpdatingUser


class TestAtlasMongoDBUserRepository:

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_user_repository.MongoClient')
    def test_should_return_user_when_create_user_is_called_with_valid_user(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.insert_one.return_value = True
        mock_collection.find_one.return_value = {"username": "User Name", "email": "user@example.com", "name": "Name",
                                                 "surname": "Surname", "role": "admin"}
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBUserRepository()
        result = repository.create_user(
            NewUser(username="User Name", password="Password", email="user@example.com", name="Name", surname="Surname",
                    role="admin"))

        assert result["username"] == "User Name"
        assert result["email"] == "user@example.com"
        assert result["name"] == "Name"
        assert result["surname"] == "Surname"
        assert result["role"] == "admin"

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_user_repository.MongoClient')
    def test_should_return_empty_dict_when_get_user_is_called_with_no_matching_username(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.find_one.return_value = None
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBUserRepository()
        result = repository.get_user("Nonexistent User Name")

        assert result == {}

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_user_repository.MongoClient')
    def test_should_return_all_users_when_get_all_users_is_called(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.find.return_value = [
            {"username": "User Name 1", "email": "user1@example.com", "name": "Name 1", "surname": "Surname 1",
             "role": "Role 1"},
            {"username": "User Name 2", "email": "user2@example.com", "name": "Name 2", "surname": "Surname 2",
             "role": "Role 2"}]
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBUserRepository()
        result = repository.get_all_users()

        assert len(result["users"]) == 2
        assert result["users"][0]["username"] == "User Name 1"
        assert result["users"][1]["username"] == "User Name 2"

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_user_repository.MongoClient')
    def test_should_return_updated_user_when_update_user_is_called_with_valid_existing_user(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.find_one.return_value = {"username": "Updated User Name", "email": "updateduser@example.com",
                                                 "name": "Updated Name", "surname": "Updated Surname",
                                                 "role": "editor"}
        mock_collection.find_one_and_update.return_value = True
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBUserRepository()
        result = repository.update_user(
            UpdatingUser(username="User Name", newUsername="Updated User Name", password="Updated Password",
                         email="updateduser@example.com", name="Updated Name", surname="Updated Surname",
                         role="editor"))

        assert result["username"] == "Updated User Name"
        assert result["email"] == "updateduser@example.com"
        assert result["name"] == "Updated Name"
        assert result["surname"] == "Updated Surname"
        assert result["role"] == "editor"

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_user_repository.MongoClient')
    def test_should_return_empty_dict_when_update_user_is_called_with_no_matching_username(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.find_one.return_value = None
        mock_collection.find_one_and_update.return_value = None
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBUserRepository()
        result = repository.update_user(
            UpdatingUser(username="Nonexistent User Name", newUsername="Updated User Name", password="Updated Password",
                         email="updateduser@example.com", name="Updated Name", surname="Updated Surname",
                         role="editor"))

        assert result == {}

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_user_repository.MongoClient')
    def test_should_return_message_when_delete_user_is_called_with_valid_username(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.delete_one.return_value = True
        mock_collection.find_one.return_value = None
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBUserRepository()
        result = repository.delete_user("User Name")

        assert result["message"] == "User User Name deleted successfully"

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_user_repository.MongoClient')
    def test_should_return_message_when_delete_user_is_called_with_invalid_username(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.delete_one.return_value = False
        mock_collection.find_one.return_value = {"username": "User Name", "email": "user@example.com", "name": "Name",
                                                 "surname": "Surname", "role": "viewer"}
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBUserRepository()
        result = repository.delete_user("Invalid User Name")

        assert result["message"] == "User Invalid User Name couldn't be deleted"
