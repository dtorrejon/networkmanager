from abc import ABCMeta, abstractmethod
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface


class IShutdownNetworkInterface(metaclass=ABCMeta):
    @abstractmethod
    def shutdown(self, interface: str) -> NetworkInterface:
        ...
