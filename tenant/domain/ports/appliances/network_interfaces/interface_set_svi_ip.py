from abc import ABCMeta, abstractmethod
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface


class ISetSviIp(metaclass=ABCMeta):

    @abstractmethod
    def set_svi_ip(self, svi: str, ip_address: str) -> NetworkInterface:
        ...