from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.vlans.vlan_trunk import VlanTrunk


class ISetVlanTrunk(metaclass=ABCMeta):

    @abstractmethod
    def set_vlan_trunk(self, interface: str, vlan_id: list[int], encapsulation: str) -> list[VlanTrunk]:
        ...
