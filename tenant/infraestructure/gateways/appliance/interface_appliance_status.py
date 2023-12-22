from abc import ABCMeta, abstractmethod


class IApplianceStatus(metaclass=ABCMeta):

    @abstractmethod
    def get(self, node_name: str) -> dict:
        ...

    @abstractmethod
    def get_all(self) -> dict:
        ...