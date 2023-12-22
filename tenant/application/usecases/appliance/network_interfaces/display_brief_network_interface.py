from tenant.domain.schemas.appliances.network_interfaces.network_interface_brief import NetworkInterfaceBrief
from tenant.domain.ports.appliances.network_interfaces.interface_display_brief_network_interface import \
    IDisplayBriefNetworkInterface
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class DisplayBriefNetworkInterface(IDisplayBriefNetworkInterface):
    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def display_brief(self) -> list[NetworkInterfaceBrief]:
        return self.appliance.display_interface_brief()
