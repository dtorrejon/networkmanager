from tenant.domain.models.repository_type import RepositoryType
from tenant.infraestructure.gateways.factories.interface_repository_factory import IRepositoryFactory
from tenant.infraestructure.adapters.repositories.atlas_mongo_db_tenant_repository import AtlasMongoDBTenantRepository
from tenant.infraestructure.gateways.interface_tenant_repository import ITenantRepository


class TenantRepositoryFactory(IRepositoryFactory):

    @staticmethod
    def get_repository(repository_type: RepositoryType) -> ITenantRepository:
        if repository_type.mongo_db_tenant:
            return AtlasMongoDBTenantRepository()
