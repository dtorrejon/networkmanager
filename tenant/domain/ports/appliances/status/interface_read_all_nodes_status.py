from abc import ABCMeta, abstractmethod


class IReadAllNodesStatus(metaclass=ABCMeta):

    @abstractmethod
    def read_all(self) -> dict:
        ...
