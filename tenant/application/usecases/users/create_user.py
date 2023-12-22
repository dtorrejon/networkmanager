from tenant.application.hasher import Hasher
from tenant.domain.schemas.users.new_user import NewUser
from tenant.domain.ports.users.interface_create_user import ICreateUser
from tenant.infraestructure.gateways.interface_user_repository import IUserRepository


class CreateUser(ICreateUser):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def create_user(self, user: NewUser) -> dict:
        user.password = Hasher.generate_hash(user.password)
        return self.user_repository.create_user(user)

