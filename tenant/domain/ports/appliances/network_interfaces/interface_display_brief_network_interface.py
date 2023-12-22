from abc import ABCMeta, abstractmethod
from tenant.domain.schemas.appliances.network_interfaces.network_interface_brief import NetworkInterfaceBrief


class IDisplayBriefNetworkInterface(metaclass=ABCMeta):
    @abstractmethod
    def display_brief(self) -> list[NetworkInterfaceBrief]:
        ...
