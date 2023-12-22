from abc import ABCMeta, abstractmethod
from typing import Optional

from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface


class IDisplayNetworkInterface(metaclass=ABCMeta):
    @abstractmethod
    def display(self, interface: Optional[str] = None) -> list[NetworkInterface]:
        ...
