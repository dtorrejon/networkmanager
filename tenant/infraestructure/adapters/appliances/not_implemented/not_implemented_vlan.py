from typing import Union

from tenant.domain.schemas.appliances.vlans.vlan_brief import VlanBrief
from tenant.domain.schemas.appliances.vlans.vlan_resume import VlanResume
from tenant.domain.schemas.appliances.vlans.vlan_trunk import VlanTrunk
from tenant.infraestructure.gateways.appliance.interface_vlan import IVlan


class NotImplementedVlan(IVlan):
    def display_vlan_brief(self) -> list[VlanBrief]:
        pass

    def set_vlan_access(self, interface: str, vlan_id: int, encapsulation: str) -> list[VlanBrief]:
        pass

    def set_vlan_native(self, interface: str, vlan_id: int, encapsulation: str) -> list[VlanTrunk]:
        pass

    def set_vlan_trunk(self, interface: str, vlan_id: list[int], encapsulation: str) -> list[VlanTrunk]:
        pass

    def remove_vlan(self, interface: str | None, vlan_id: Union[int, str]) -> VlanResume:
        pass

    def display_vlan_trunk(self) -> list[VlanTrunk]:
        pass