from typing import Optional

from tenant.domain.ports.appliances.network_interfaces.interface_display_network_interface import IDisplayNetworkInterface
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class DisplayNetworkInterfaces(IDisplayNetworkInterface):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def display(self, interface: Optional[str] = None) -> list[NetworkInterface]:
        return self.appliance.display(interface)
