from abc import ABCMeta, abstractmethod


class IHasher(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def compare_hash(cls, plain_password: str, hashed_password: str) -> bool:
        ...

    @classmethod
    @abstractmethod
    def generate_hash(cls, plain_text: str) -> str:
        ...
