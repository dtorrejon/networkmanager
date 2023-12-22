from abc import ABCMeta, abstractmethod


class IReadNodeStatus(metaclass=ABCMeta):

    @abstractmethod
    def read(self) -> dict:
        ...
