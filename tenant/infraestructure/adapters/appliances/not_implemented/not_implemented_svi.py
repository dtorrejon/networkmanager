from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.infraestructure.gateways.appliance.interface_svi import ISvi


class NotImplementedSvi(ISvi):

    def __init__(self):
        self.message = NetworkInterface(**{
                    "name": "Not Implemented",
                    "description": "Function Not available for this network element",
                    "macAddress": "-",
                    "ipAddress": "-",
                    "mtu": 0,
                    "status": "-",
                    "protocol": "-"
                })
    def create_svi(self, vlan_id: str) -> NetworkInterface:
        return self.message

    def set_svi_ip(self, svi: str, ip_address: str) -> NetworkInterface:
        return self.message

    def delete_svi(self, vlan_id: str) -> list[NetworkInterface]:
        return[self.message]