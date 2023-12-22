from tenant.domain.ports.users.interface_read_all_users import IReadAllUsers
from tenant.infraestructure.gateways.interface_user_repository import IUserRepository


class ReadAllUsers(IReadAllUsers):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def read_all_users(self) -> dict:
        return self.user_repository.get_all_users()

