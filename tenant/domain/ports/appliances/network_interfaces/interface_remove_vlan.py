from abc import ABCMeta, abstractmethod
from typing import Union

from tenant.domain.schemas.appliances.vlans.vlan_resume import VlanResume


class IRemoveVlan(metaclass=ABCMeta):

    @abstractmethod
    def remove_vlan(self, interface: str, vlan_id: Union[int, str]) -> VlanResume:
        ...
