from typing import Union
from netmiko import BaseConnection

from tenant.domain.schemas.appliances.vlans.vlan_brief import VlanBrief
from tenant.domain.schemas.appliances.vlans.vlan_resume import VlanResume
from tenant.domain.schemas.appliances.vlans.vlan_trunk import VlanTrunk
from tenant.infraestructure.adapters.appliances.cisco.formatter.vlan.cisco_ios_display_vlan_brief_formatter import \
    CiscoIosDisplayVlanBriefFormatter
from tenant.infraestructure.adapters.appliances.cisco.formatter.vlan.cisco_ios_display_vlan_formatter import \
    CiscoDisplayVlanTrunkFormatter
from tenant.infraestructure.gateways.appliance.interface_vlan import IVlan


class CiscoIosVlan(IVlan):
    def __init__(self, connect: BaseConnection):
        self.connect: BaseConnection = connect

    def display_vlan_brief(self) -> list[VlanBrief]:
        self.connect.secret = self.connect.password
        self.connect.enable()
        output = self.connect.send_command_timing(f"show vlan brief")
        return CiscoIosDisplayVlanBriefFormatter().format(output)

    def display_vlan_trunk(self) -> list[VlanTrunk]:
        self.connect.secret = self.connect.password
        self.connect.enable()
        output = self.connect.send_command_timing(f"show interfaces trunk")
        return CiscoDisplayVlanTrunkFormatter().format(output)

    def set_vlan_access(self, interface: str, vlan_id: int, encapsulation: str = "dot1q") -> list[VlanBrief]:
        self._select_interface(interface)
        self.connect.send_command_timing(f"switchport trunk encapsulation {encapsulation}")
        self.connect.send_command_timing(f"switchport mode access")
        self.connect.send_command_timing(f"switchport access vlan {vlan_id} ")
        self._write()
        return self.display_vlan_brief()

    def set_vlan_trunk(self, interface: str, vlan_id: list[int], encapsulation: str = "dot1q") -> list[VlanTrunk]:
        self._select_interface(interface)
        r = self.connect.send_command_timing(f"switchport trunk encapsulation {encapsulation}")
        r = self.connect.send_command_timing(f"switchport mode trunk")
        vlans_out = ','.join(map(str, vlan_id))
        r = self.connect.send_command_timing(f"switchport trunk allowed vlan {vlans_out}")
        self._write()
        return self.display_vlan_trunk()

    def set_vlan_native(self, interface: str, vlan_id: int, encapsulation: str = "dot1q") -> list[VlanTrunk]:
        self._select_interface(interface)
        self.connect.send_command_timing(f"switchport trunk encapsulation {encapsulation}")
        self.connect.send_command_timing(f"switchport mode trunk")
        self.connect.send_command_timing(f"switchport trunk native vlan {vlan_id}")
        self._write()
        return self.display_vlan_trunk()

    def remove_vlan(self, interface: str, vlan_id: Union[int, str]) -> VlanResume:
        self.connect.secret = self.connect.password
        self.connect.enable()
        self.connect.send_command_timing(f"configure terminal")

        if interface is None and isinstance(vlan_id, int):
            self.connect.send_command_timing(f"no vlan {vlan_id}")
        elif isinstance(vlan_id, str) and vlan_id == "all":
            self.connect.send_command_timing(f"interface {interface}")
            self.connect.send_command_timing(f"switchport trunk allowed vlan none")
        else:
            self.connect.send_command_timing(f"interface {interface}")
            self.connect.send_command_timing(f"switchport trunk allowed vlan remove {vlan_id}")

        self._write()

        return VlanResume(vlanAccess=self.display_vlan_brief(), vlanTrunk=self.display_vlan_trunk())

    def _select_interface(self, interface: str):
        self.connect.secret = self.connect.password
        self.connect.enable()
        self.connect.send_command_timing(f"configure terminal")
        self.connect.send_command_timing(f"interface {interface}")

    def _delete_interface(self, interface: str):
        self.connect.secret = self.connect.password
        self.connect.enable()
        self.connect.send_command_timing(f"configure terminal")
        self.connect.send_command_timing(f"no interface {interface}")

    def _write(self):
        self.connect.send_command_timing(f"end")
        self.connect.send_command_timing(f"write")
