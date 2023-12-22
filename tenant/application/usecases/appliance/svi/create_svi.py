from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.domain.ports.appliances.network_interfaces.interface_create_svi import ICreateSVI
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class CreateSVI(ICreateSVI):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def create(self, vlan_id: str) -> NetworkInterface:
        return self.appliance.create_svi(vlan_id)
