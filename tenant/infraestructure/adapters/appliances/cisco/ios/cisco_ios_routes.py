from netmiko import BaseConnection

from tenant.domain.schemas.appliances.diagnostics.route import Route
from tenant.infraestructure.adapters.appliances.cisco.formatter.rotuing.cisco_ios_routing_table_formatter import \
    CiscoIosRoutingTableFormatter
from tenant.infraestructure.gateways.appliance.interface_routes import IRoutes


class CiscoIosStaticRoutes(IRoutes):

    def __init__(self, connect: BaseConnection):
        self.connect: BaseConnection = connect

    def routing_table(self) -> list[Route]:
        self.connect.secret = self.connect.password
        self.connect.enable()
        response = self.connect.send_command(f"show ip route")

        return CiscoIosRoutingTableFormatter().format(response)

    def set_default_gateway(self, ip: str) -> list[Route]:
        self._enable()
        self.connect.send_config_set(f"ip route 0.0.0.0 0.0.0.0 {ip}")
        self._write()
        resp = self.routing_table()
        return resp

    def set_static_route(self, ip_and_mask: str, ip_next_hop: str) -> list[Route]:
        self._enable()
        self.connect.send_command_timing(f"ip route {ip_and_mask} {ip_next_hop}")
        self._write()
        return self.routing_table()

    def _enable(self):
        self.connect.secret = self.connect.password
        self.connect.enable()

    def _write(self):
        self.connect.send_command_timing(f"end")
        self.connect.send_command_timing(f"write")
