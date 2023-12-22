from abc import ABCMeta, abstractmethod
from typing import Optional

from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.domain.schemas.appliances.network_interfaces.network_interface_brief import NetworkInterfaceBrief


class INetworkInterfaces(metaclass=ABCMeta):

    @abstractmethod
    def display(self, interface: Optional[str] = None) -> list[NetworkInterface]:
        ...

    @abstractmethod
    def display_interface_brief(self) -> list[NetworkInterfaceBrief]:
        ...

    @abstractmethod
    def no_shutdown(self, interface: str) -> NetworkInterface:
        ...

    @abstractmethod
    def shutdown(self, interface: str) -> NetworkInterface:
        ...

    @abstractmethod
    def set_ip(self, interface: str, ip_address: str) -> NetworkInterface:
        ...

    @abstractmethod
    def set_description(self, interface: str, description: str) -> NetworkInterface:
        ...

