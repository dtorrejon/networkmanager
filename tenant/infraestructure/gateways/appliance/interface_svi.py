from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface


class ISvi(metaclass=ABCMeta):
    @abstractmethod
    def create_svi(self, vlan_id: str) -> NetworkInterface:
        ...

    @abstractmethod
    def set_svi_ip(self, svi: str, ip_address: str) -> NetworkInterface:
        ...

    @abstractmethod
    def delete_svi(self, vlan_id: str) -> list[NetworkInterface]:
        ...
