
from tenant.domain.ports.appliances.routing.interface_set_static_route import ISetStaticRoute
from tenant.domain.schemas.appliances.diagnostics.route import Route
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class SetStaticRoute(ISetStaticRoute):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def set_static_route(self, ip_and_mask_in_cidr: str, ip_next_hop: str) -> list[Route]:
        return self.appliance.set_static_route(ip_and_mask_in_cidr, ip_next_hop)
