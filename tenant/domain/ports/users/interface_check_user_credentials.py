from abc import ABCMeta, abstractmethod


class ICheckUserCredentials(metaclass=ABCMeta):
    @abstractmethod
    def check_credentials(self, username: str, password: str) -> bool:
        ...
