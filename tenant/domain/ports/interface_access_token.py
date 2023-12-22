from abc import ABCMeta, abstractmethod


class IAccessToken(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def generate_token(cls, **kwargs) -> dict:
        ...

    @classmethod
    @abstractmethod
    def decode_token(cls, **kwargs) -> dict:
        ...
