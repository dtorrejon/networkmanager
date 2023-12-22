from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.domain.ports.appliances.network_interfaces.interface_delete_svi import IDeleteSVI
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class DeleteSVI(IDeleteSVI):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def delete(self, vlan_id: str) -> list[NetworkInterface]:
        return self.appliance.delete_svi(vlan_id)
