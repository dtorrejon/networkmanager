from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.users.existing_user import ExistingUser


class IUpdateUser(metaclass=ABCMeta):

    @abstractmethod
    def update_user(self, user: ExistingUser) -> dict:
        ...
