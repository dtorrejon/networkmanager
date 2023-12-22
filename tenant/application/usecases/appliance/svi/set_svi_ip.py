from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.domain.ports.appliances.network_interfaces.interface_set_svi_ip import ISetSviIp
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class SetSviIp(ISetSviIp):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def set_svi_ip(self, svi: str, ip_address: str) -> NetworkInterface:
        return self.appliance.set_svi_ip(svi, ip_address)