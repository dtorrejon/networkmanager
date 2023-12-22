from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.users.new_user import NewUser


class ICreateUser(metaclass=ABCMeta):

    @abstractmethod
    def create_user(self, user: NewUser) -> dict:
        ...
