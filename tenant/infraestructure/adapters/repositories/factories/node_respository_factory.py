from tenant.domain.models.repository_type import RepositoryType
from tenant.infraestructure.adapters.repositories.atlas_mongo_db_node_repository import AtlasMongoDBNodeRepository
from tenant.infraestructure.gateways.interface_node_repository import INodeRepository
from tenant.infraestructure.gateways.factories.interface_repository_factory import IRepositoryFactory


class NodeRepositoryFactory(IRepositoryFactory):

    @staticmethod
    def get_repository(repository_type: RepositoryType) -> INodeRepository:
        if repository_type.mongo_db_user:
            return AtlasMongoDBNodeRepository()
