from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.diagnostics.route import Route


class ISetStaticRoute(metaclass=ABCMeta):
    @abstractmethod
    def set_static_route(self, ip_and_mask_in_cidr: str, ip_next_hop: str) -> list[Route]:
        ...
