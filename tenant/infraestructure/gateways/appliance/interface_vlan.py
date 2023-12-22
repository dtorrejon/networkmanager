from abc import ABCMeta, abstractmethod
from typing import Union

from tenant.domain.schemas.appliances.vlans.vlan_brief import VlanBrief
from tenant.domain.schemas.appliances.vlans.vlan_resume import VlanResume
from tenant.domain.schemas.appliances.vlans.vlan_trunk import VlanTrunk


class IVlan(metaclass=ABCMeta):

    @abstractmethod
    def display_vlan_brief(self) -> list[VlanBrief]:
        ...

    @abstractmethod
    def set_vlan_access(self, interface: str, vlan_id: int, encapsulation: str) -> list[VlanBrief]:
        ...

    @abstractmethod
    def set_vlan_native(self, interface: str, vlan_id: int, encapsulation: str) -> list[VlanTrunk]:
        ...

    @abstractmethod
    def set_vlan_trunk(self, interface: str, vlan_id: list[int], encapsulation: str) -> list[VlanTrunk]:
        ...

    @abstractmethod
    def remove_vlan(self, interface: str, vlan_id: Union[int, str]) -> VlanResume:
        ...

    @abstractmethod
    def display_vlan_trunk(self) -> list[VlanTrunk]:
        ...
