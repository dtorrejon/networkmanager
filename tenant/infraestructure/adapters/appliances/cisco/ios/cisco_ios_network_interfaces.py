import ipaddress
from typing import Optional
from netmiko import BaseConnection

from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.domain.schemas.appliances.network_interfaces.network_interface_brief import NetworkInterfaceBrief
from tenant.infraestructure.adapters.appliances.cisco.formatter.network_interfaces.cisco_ios_display_interface_brief_formatter import \
    CiscoIosDisplayInterfaceBriefFormatter
from tenant.infraestructure.adapters.appliances.cisco.formatter.network_interfaces.cisco_ios_display_interface_formatter import \
    CiscoIosDisplayInterfaceInterfaceFormatter
from tenant.infraestructure.gateways.appliance.interface_network_interfaces import INetworkInterfaces


class CiscoIosNetworkInterfaces(INetworkInterfaces):

    def __init__(self, connect: BaseConnection):
        self.connect: BaseConnection = connect

    def display(self, interface: Optional[str] = None) -> list[NetworkInterface]:
        if interface is None:
            interface = ""
        self.connect.secret = self.connect.password
        self.connect.enable()
        output = self.connect.send_command_timing(f"show interfaces {interface}")
        return CiscoIosDisplayInterfaceInterfaceFormatter().format(output)

    def display_interface_brief(self) -> list[NetworkInterfaceBrief]:
        self.connect.secret = self.connect.password
        self.connect.enable()
        output = self.connect.send_command_timing(f"show ip interface brief")

        return CiscoIosDisplayInterfaceBriefFormatter().format(output)

    def no_shutdown(self, interface: str) -> NetworkInterface:
        self._select_interface(interface)
        self.connect.send_command_timing(f"no shutdown")
        self._write()
        return self.display(interface)[0]

    def shutdown(self, interface: str) -> NetworkInterface:
        self._select_interface(interface)
        self.connect.send_command_timing(f"shutdown")
        self._write()
        return self.display(interface)[0]

    def set_ip(self, interface: str, ip_address_and_mask: str) -> NetworkInterface:
        ip = ipaddress.IPv4Interface(ip_address_and_mask).ip
        mask = ipaddress.IPv4Interface(ip_address_and_mask).netmask
        self._select_interface(interface)
        self.connect.send_command_timing(f"no switchport")
        self.connect.send_command_timing(f"ip address {ip} {mask}")
        self._write()
        return self.display(interface)[0]

    def set_description(self, interface: str, description: str) -> NetworkInterface:
        self._select_interface(interface)
        self.connect.send_command_timing(f"description {description}")
        self._write()
        return self.display(interface)[0]


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
