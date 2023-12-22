from abc import ABCMeta, abstractmethod

from pydantic import EmailStr


class IReadUser(metaclass=ABCMeta):

    @abstractmethod
    def read_user(self, username: str) -> dict:
        ...

    @abstractmethod
    def read_user_by_mail(self, email: EmailStr) -> dict:
        ...
