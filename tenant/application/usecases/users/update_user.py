from tenant.application.hasher import Hasher
from tenant.domain.schemas.users.updating_user import UpdatingUser
from tenant.domain.ports.users.interface_update_user import IUpdateUser
from tenant.infraestructure.gateways.interface_user_repository import IUserRepository


class UpdateUser(IUpdateUser):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def update_user(self, user: UpdatingUser) -> dict:
        if user.password != "":
            user.password = Hasher.generate_hash(user.password)
        return self.user_repository.update_user(user)
