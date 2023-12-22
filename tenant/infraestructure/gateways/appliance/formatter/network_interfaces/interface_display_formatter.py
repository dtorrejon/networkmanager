from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface


class IdisplayInterfaceFormatter(metaclass=ABCMeta):

    @abstractmethod
    def format(self, display_text: str) -> list[NetworkInterface]:
        ...
