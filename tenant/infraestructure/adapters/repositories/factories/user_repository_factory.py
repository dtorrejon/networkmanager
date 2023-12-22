from tenant.domain.models.repository_type import RepositoryType
from tenant.infraestructure.gateways.factories.interface_repository_factory import IRepositoryFactory
from tenant.infraestructure.adapters.repositories.atlas_mongo_db_user_repository import AtlasMongoDBUserRepository
from tenant.infraestructure.gateways.interface_user_repository import IUserRepository


class UserRepositoryFactory(IRepositoryFactory):

    @staticmethod
    def get_repository(repository_type: RepositoryType) -> IUserRepository:
        if repository_type.mongo_db_user:
            return AtlasMongoDBUserRepository()
