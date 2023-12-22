
from tenant.domain.schemas.appliances.vlans.vlan_trunk import VlanTrunk
from tenant.domain.ports.appliances.network_interfaces.interface_set_vlan_native import ISetVlanNative
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class SetVlanNative(ISetVlanNative):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def set_vlan_native(self, interface: str, vlan_id: int, encapsulation: str) -> list[VlanTrunk]:
        return self.appliance.set_vlan_native(interface, vlan_id, encapsulation)