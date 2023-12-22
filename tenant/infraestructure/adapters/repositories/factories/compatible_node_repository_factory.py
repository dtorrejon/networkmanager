from tenant.domain.models.repository_type import RepositoryType
from tenant.infraestructure.adapters.repositories.atlas_mongo_db_compatible_repository import \
    AtlasMongoDBCompatibleNodeRepository
from tenant.infraestructure.gateways.interface_compatible_node_repository import ICompatibleNodeRepository
from tenant.infraestructure.gateways.factories.interface_repository_factory import IRepositoryFactory


class CompatibleNodeRepositoryFactory(IRepositoryFactory):

    @staticmethod
    def get_repository(repository_type: RepositoryType) -> ICompatibleNodeRepository:
        if repository_type.mongo_db_user:
            return AtlasMongoDBCompatibleNodeRepository()
