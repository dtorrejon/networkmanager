from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.domain.ports.appliances.network_interfaces.interface_no_shutdown_network_interface import \
    INoShutdownNetworkInterface
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class NoShutdownNetworkInterface(INoShutdownNetworkInterface):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def no_shutdown(self, interface: str) -> NetworkInterface:
        return self.appliance.no_shutdown(interface)
