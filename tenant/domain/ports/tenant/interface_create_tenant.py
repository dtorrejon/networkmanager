from abc import ABCMeta, abstractmethod


class ICreateTenant(metaclass=ABCMeta):

    @abstractmethod
    def create(self, tenant: dict) -> dict:
        ...
