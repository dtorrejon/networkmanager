from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.diagnostics.route import Route


class ILaunchRoutingTable(metaclass=ABCMeta):

    @abstractmethod
    def routing_table(self) -> list[Route]:
        ...
