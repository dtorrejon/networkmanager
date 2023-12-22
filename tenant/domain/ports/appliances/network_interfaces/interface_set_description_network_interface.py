from abc import ABCMeta, abstractmethod
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface


class ISetDescriptionNetworkInterface(metaclass=ABCMeta):
    @abstractmethod
    def set_description(self, interface: str, description: str) -> NetworkInterface:
        ...
