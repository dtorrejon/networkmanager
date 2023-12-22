
from tenant.domain.ports.appliances.routing.interface_set_default_gateway import ISetDefaultGateway
from tenant.domain.schemas.appliances.diagnostics.route import Route
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class SetDefaultGateway(ISetDefaultGateway):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def set_default_gateway(self, ip: str) -> list[Route]:
        return self.appliance.set_default_gateway(ip)

