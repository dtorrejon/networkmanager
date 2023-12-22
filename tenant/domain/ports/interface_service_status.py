from abc import ABCMeta, abstractmethod


class IServiceStatus(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def status(hostname: str, port: int) -> bool:
        ...
