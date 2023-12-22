from unittest.mock import Mock, patch
from tenant.infraestructure.adapters.repositories.atlas_mongo_db_tenant_repository import \
    AtlasMongoDBTenantRepository
from tenant.domain.schemas.tenants.tenant import Tenant
from tenant.domain.schemas.tenants.existing_tenant import ExistingTenant


class TestAtlasMongoDBTenantRepository:

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_tenant_repository.MongoClient')
    def test_should_return_tenant_when_get_tenant_is_called(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.find_one.return_value = {"name": "Tenant-Name", "phone": "123456789",
                                                 "address": "Tenant Address"}
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBTenantRepository()
        result = repository.get_tenant()

        assert isinstance(result, Tenant)
        assert result.name == "Tenant-Name"
        assert result.phone == "123456789"
        assert result.address == "Tenant Address"
    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_tenant_repository.MongoClient')
    def test_should_return_empty_dict_when_get_tenant_is_called_and_no_tenant_exists(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.find_one.return_value = None
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBTenantRepository()
        result = repository.get_tenant()

        assert result == {}

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_tenant_repository.MongoClient')
    def test_should_return_updated_tenant_when_update_tenant_is_called(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.find_one.return_value = {"name": "Updated Tenant Name", "phone": "987654321",
                                                 "address": "Updated Tenant Address"}
        mock_collection.find_one_and_update.return_value = True
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBTenantRepository()
        result = repository.update_tenant(
            ExistingTenant(name="Updated Tenant Name", phone="987654321", address="Updated Tenant Address"))

        assert isinstance(result, Tenant)
        assert result.name == "Updated Tenant Name"
        assert result.phone == "987654321"
        assert result.address == "Updated Tenant Address"

    @staticmethod
    @patch('tenant.infraestructure.adapters.repositories.atlas_mongo_db_tenant_repository.MongoClient')
    def test_should_return_empty_dict_when_update_tenant_is_called_and_no_tenant_exists(mock_mongo_client):
        mock_collection = Mock()
        mock_collection.find_one.return_value = None
        mock_collection.find_one_and_update.return_value = None
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        repository = AtlasMongoDBTenantRepository()
        result = repository.update_tenant(
            ExistingTenant(name="Updated Tenant Name", phone="987654321", address="Updated Tenant Address"))

        assert result == {}
