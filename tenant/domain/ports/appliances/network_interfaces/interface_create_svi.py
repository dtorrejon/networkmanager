from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface


class ICreateSVI(metaclass=ABCMeta):
    @abstractmethod
    def create(self, vlan_id: str) -> NetworkInterface:
        ...