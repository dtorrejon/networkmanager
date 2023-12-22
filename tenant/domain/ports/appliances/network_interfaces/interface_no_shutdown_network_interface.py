from abc import ABCMeta, abstractmethod
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface


class INoShutdownNetworkInterface(metaclass=ABCMeta):
    @abstractmethod
    def no_shutdown(self, interface: str) -> NetworkInterface:
        ...
