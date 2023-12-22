from tenant.domain.ports.users.interface_delete_user import IDeleteUser
from tenant.infraestructure.gateways.interface_user_repository import IUserRepository


class DeleteUser(IDeleteUser):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def delete_user(self, username: str) -> dict:
        return self.user_repository.delete_user(username)
