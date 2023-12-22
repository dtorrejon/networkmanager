from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.vlans.vlan_brief import VlanBrief


class IdisplayVlanBriefFormatter(metaclass=ABCMeta):

    @abstractmethod
    def format(self, display_text: str) -> list[VlanBrief]:
        ...