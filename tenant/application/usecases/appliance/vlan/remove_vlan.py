from typing import Union

from tenant.domain.schemas.appliances.vlans.vlan_resume import VlanResume
from tenant.domain.ports.appliances.network_interfaces.interface_remove_vlan import IRemoveVlan
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class RemoveVlan(IRemoveVlan):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def remove_vlan(self, interface: str, vlan_id: Union[int, str]) -> VlanResume:
        return self.appliance.remove_vlan(interface, vlan_id)
