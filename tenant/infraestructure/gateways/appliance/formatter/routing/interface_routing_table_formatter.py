from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.diagnostics.route import Route


class IRoutingTableFormatter(metaclass=ABCMeta):

    @abstractmethod
    def format(self, routing_table_text: str) -> Route:
        ...
