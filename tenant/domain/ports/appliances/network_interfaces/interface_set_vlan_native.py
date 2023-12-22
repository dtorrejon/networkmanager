from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.vlans.vlan_trunk import VlanTrunk


class ISetVlanNative(metaclass=ABCMeta):

    @abstractmethod
    def set_vlan_native(self, interface: str, vlan_id: int, encapsulation: str) -> list[VlanTrunk]:
        ...
