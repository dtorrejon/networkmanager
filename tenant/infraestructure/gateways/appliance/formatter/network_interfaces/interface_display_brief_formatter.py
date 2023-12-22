from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.network_interfaces.network_interface_brief import NetworkInterfaceBrief


class IdisplayBriefFormatter(metaclass=ABCMeta):

    @abstractmethod
    def format(self, display_text: str) -> list[NetworkInterfaceBrief]:
        ...
