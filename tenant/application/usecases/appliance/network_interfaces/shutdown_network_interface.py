from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.domain.ports.appliances.network_interfaces.interface_shutdown_network_interface import \
    IShutdownNetworkInterface
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class ShutdownNetworkInterface(IShutdownNetworkInterface):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def shutdown(self, interface: str) -> NetworkInterface:
        return self.appliance.shutdown(interface)
