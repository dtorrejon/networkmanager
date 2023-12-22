from abc import ABCMeta, abstractmethod
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface


class ISetIPNetworkInterface(metaclass=ABCMeta):

    @abstractmethod
    def set_ip(self, interface: str, ip_address: str) -> NetworkInterface:
        ...
