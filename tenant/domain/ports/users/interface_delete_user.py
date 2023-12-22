from abc import ABCMeta, abstractmethod


class IDeleteUser(metaclass=ABCMeta):

    @abstractmethod
    def delete_user(self, username: str) -> dict:
        ...
