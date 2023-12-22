from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.vlans.vlan_brief import VlanBrief


class ISetVlanAccess(metaclass=ABCMeta):

    @abstractmethod
    def set_vlan_access(self, interface: str, vlan_id: int, encapsulation: str) -> list[VlanBrief]:
        ...
