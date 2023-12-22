from abc import ABCMeta, abstractmethod

from pydantic import EmailStr

from tenant.domain.schemas.users.updating_user import UpdatingUser
from tenant.domain.schemas.users.new_user import NewUser


class IUserRepository(metaclass=ABCMeta):

    @abstractmethod
    def create_user(self, user: NewUser) -> dict:
        ...

    @abstractmethod
    def get_user(self, username: str) -> dict:
        ...

    @abstractmethod
    def get_user_by_mail(self, email: EmailStr) -> dict:
        ...

    @abstractmethod
    def get_all_users(self) -> dict:
        ...

    @abstractmethod
    def update_user(self, user: UpdatingUser) -> dict:
        ...

    @abstractmethod
    def delete_user(self, username: str) -> dict:
        ...

    def read_password(self, username: str) -> dict:
        ...
