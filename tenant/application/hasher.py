from passlib.context import CryptContext
from tenant.domain.ports.haser_interface import IHasher


class Hasher(IHasher):
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def compare_hash(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.context.verify(plain_password, hashed_password)

    @classmethod
    def generate_hash(cls, plain_text: str) -> str:
        return cls.context.hash(plain_text)
