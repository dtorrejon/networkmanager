from abc import ABCMeta, abstractmethod


class IReadAllUsers(metaclass=ABCMeta):

    @abstractmethod
    def read_all_users(self) -> dict:
        ...
