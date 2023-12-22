from tenant.domain.schemas.appliances.vlans.vlan_trunk import VlanTrunk
from tenant.domain.ports.appliances.network_interfaces.interface_set_vlan_trunk import ISetVlanTrunk
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class SetVlanTrunk(ISetVlanTrunk):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def set_vlan_trunk(self, interface: str, vlan_ids: list[int], encapsulation: str) -> list[VlanTrunk]:
        return self.appliance.set_vlan_trunk(interface, vlan_ids, encapsulation)
