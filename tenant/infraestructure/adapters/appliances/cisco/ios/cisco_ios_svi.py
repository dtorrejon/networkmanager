import ipaddress
from typing import Optional

from netmiko import BaseConnection

from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.infraestructure.adapters.appliances.cisco.ios.cisco_ios_network_interfaces import \
    CiscoIosNetworkInterfaces
from tenant.infraestructure.gateways.appliance.interface_svi import ISvi


class CiscoIosSvi(ISvi):
    def __init__(self, connect: BaseConnection):
        self.connect: BaseConnection = connect
        self.display = CiscoIosNetworkInterfaces(connect)

    def create_svi(self, vlan_id: str) -> NetworkInterface:
        if "vlan" not in vlan_id.lower():
            vlan_id = f"Vlan{vlan_id}"
        self._select_interface(vlan_id)
        self._write()
        return self._display(vlan_id)[0]

    def set_svi_ip(self, svi: str, ip_address_and_mask: str) -> NetworkInterface:
        ip = ipaddress.IPv4Interface(ip_address_and_mask).ip
        mask = ipaddress.IPv4Interface(ip_address_and_mask).netmask
        self._select_interface(svi)
        self.connect.send_command_timing(f"ip address {ip} {mask}")
        self._write()
        return self._display(svi)[0]

    def delete_svi(self, vlan_id: str) -> list[NetworkInterface]:
        if "vlan" not in vlan_id.lower():
            vlan_id = f"Vlan{vlan_id}"
        self._delete_interface(vlan_id)
        self._write()
        return self._display()

    def _display(self, interface: Optional[str] = None) -> list[NetworkInterface]:
        return CiscoIosNetworkInterfaces(self.connect).display(interface)

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
