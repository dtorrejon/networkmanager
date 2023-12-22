from pydantic import EmailStr

from tenant.domain.ports.users.interface_read_user import IReadUser
from tenant.infraestructure.gateways.interface_user_repository import IUserRepository


class ReadUser(IReadUser):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def read_user(self, username: str) -> dict:
        return self.user_repository.get_user(username)

    def read_user_by_mail(self, email: EmailStr) -> dict:
        return self.user_repository.get_user_by_mail(email)
