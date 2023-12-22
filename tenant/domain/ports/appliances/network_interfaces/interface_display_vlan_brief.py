from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.vlans.vlan_brief import VlanBrief


class IDisplayVlanBrief(metaclass=ABCMeta):

    @abstractmethod
    def display_brief(self) -> list[VlanBrief]:
        ...
