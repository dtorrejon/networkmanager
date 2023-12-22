from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface


class IDeleteSVI(metaclass=ABCMeta):
    @abstractmethod
    def delete(self, vlan_id: str) -> list[NetworkInterface]:
        ...
