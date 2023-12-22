from tenant.domain.models.repository_type import RepositoryType
from tenant.infraestructure.adapters.repositories.create_atlas_mongo_db_tenant_repository import \
    CreateAtlasMongoDBTenantRepository
from tenant.infraestructure.gateways.factories.interface_create_tenant_repository import ICreateTenantRepository
from tenant.infraestructure.gateways.factories.interface_repository_factory import IRepositoryFactory


class CreateTenantRepositoryFactory(IRepositoryFactory):

    @staticmethod
    def get_repository(repository_type: RepositoryType) -> ICreateTenantRepository:

        if repository_type.mongo_db_create_tenant:
            return CreateAtlasMongoDBTenantRepository()
