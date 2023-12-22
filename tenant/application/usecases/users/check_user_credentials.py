from tenant.domain.ports.haser_interface import IHasher
from tenant.domain.ports.users.interface_check_user_credentials import ICheckUserCredentials
from tenant.infraestructure.gateways.interface_user_repository import IUserRepository


class CheckUserCredentials(ICheckUserCredentials):

    def __init__(self, user_repository: IUserRepository, hasher: IHasher):
        self.user_repository = user_repository
        self.hasher = hasher

    def check_credentials(self, username: str, password: str) -> bool:
        db_credentials: dict = self.user_repository.read_password(username)
        if db_credentials is None:
            return False
        else:
            return self.hasher.compare_hash(password, db_credentials.get("password"))
