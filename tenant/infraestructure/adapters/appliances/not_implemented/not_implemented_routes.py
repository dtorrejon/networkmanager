from tenant.domain.schemas.appliances.diagnostics.route import Route
from tenant.infraestructure.gateways.appliance.interface_routes import IRoutes


class NotImplementedRoutes(IRoutes):
    def routing_table(self) -> Route:
        pass

    def set_default_gateway(self, ip: str) -> Route:
        pass

    def set_static_route(self, ip_and_mask_in_cidr: str, ip_next_hop: str) -> Route:
        pass