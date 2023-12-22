
from tenant.domain.ports.appliances.routing.interface_launch_routing_table import ILaunchRoutingTable
from tenant.domain.schemas.appliances.diagnostics.route import Route
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class LaunchRoutingTable(ILaunchRoutingTable):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def routing_table(self) -> list[Route]:
        return self.appliance.routing_table()
