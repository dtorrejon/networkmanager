from typing import Optional

from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.domain.schemas.appliances.network_interfaces.network_interface_brief import NetworkInterfaceBrief
from tenant.infraestructure.gateways.appliance.interface_network_interfaces import INetworkInterfaces


class NotImplementedNetworkInterfaces(INetworkInterfaces):
    def display(self, interface: Optional[str] = None) -> list[NetworkInterface]:
        pass

    def display_interface_brief(self) -> list[NetworkInterfaceBrief]:
        pass

    def no_shutdown(self, interface: str) -> NetworkInterface:
        pass

    def shutdown(self, interface: str) -> NetworkInterface:
        pass

    def set_ip(self, interface: str, ip_address: str) -> NetworkInterface:
        pass

    def set_description(self, interface: str, description: str) -> NetworkInterface:
        pass