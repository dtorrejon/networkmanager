from tenant.domain.schemas.appliances.vlans.vlan_trunk import VlanTrunk
from tenant.domain.ports.appliances.network_interfaces.interface_display_vlan_trunk import IDisplayVlanTrunk
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class DisplayVlanTrunk(IDisplayVlanTrunk):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def display(self) -> list[VlanTrunk]:
        return self.appliance.display_vlan_trunk()
