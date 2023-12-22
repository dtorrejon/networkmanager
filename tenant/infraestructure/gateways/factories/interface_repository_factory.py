from abc import abstractmethod, ABCMeta

from tenant.domain.models.repository_type import RepositoryType


class IRepositoryFactory(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_repository(repository_type: RepositoryType) -> object:
        ...
