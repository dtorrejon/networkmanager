
from tenant.domain.schemas.appliances.vlans.vlan_brief import VlanBrief
from tenant.domain.ports.appliances.network_interfaces.interface_set_vlan_access import ISetVlanAccess
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class SetVlanAccess(ISetVlanAccess):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def set_vlan_access(self, interface: str, vlan_id: int, encapsulation: str) -> list[VlanBrief]:
        return self.appliance.set_vlan_access(interface, vlan_id, encapsulation)
