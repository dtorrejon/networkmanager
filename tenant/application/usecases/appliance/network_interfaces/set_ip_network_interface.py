from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.domain.ports.appliances.network_interfaces.interface_set_ip_network_interface import ISetIPNetworkInterface
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class SetIPNetworkInterface(ISetIPNetworkInterface):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def set_ip(self, interface: str, ip_address: str) -> NetworkInterface:
        return self.appliance.set_ip(interface, ip_address)
