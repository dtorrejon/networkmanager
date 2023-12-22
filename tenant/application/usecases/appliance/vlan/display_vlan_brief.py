from tenant.domain.schemas.appliances.vlans.vlan_brief import VlanBrief
from tenant.domain.ports.appliances.network_interfaces.interface_display_vlan_brief import IDisplayVlanBrief
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class DisplayVlanBrief(IDisplayVlanBrief):
    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def display_brief(self) -> list[VlanBrief]:
        return self.appliance.display_vlan_brief()
