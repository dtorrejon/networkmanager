from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.diagnostics.route import Route


class ISetDefaultGateway(metaclass=ABCMeta):
    @abstractmethod
    def set_default_gateway(self, ip: str) -> list[Route]:
        ...
