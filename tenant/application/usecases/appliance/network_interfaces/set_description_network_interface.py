from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.domain.ports.appliances.network_interfaces.interface_set_description_network_interface import \
    ISetDescriptionNetworkInterface
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class SetDescriptionNetworkInterface(ISetDescriptionNetworkInterface):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def set_description(self, interface :str, description: str) -> NetworkInterface:
        return self.appliance.set_description(interface, description)
