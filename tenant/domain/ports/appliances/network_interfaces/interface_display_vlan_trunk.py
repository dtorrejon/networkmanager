from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.vlans.vlan_trunk import VlanTrunk


class IDisplayVlanTrunk(metaclass=ABCMeta):

    @abstractmethod
    def display(self) -> list[VlanTrunk]:
        ...