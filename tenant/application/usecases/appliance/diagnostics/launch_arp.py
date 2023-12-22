from tenant.domain.schemas.appliances.diagnostics.arp import Arp
from tenant.domain.ports.appliances.diagnostics.interface_launch_arp import ILaunchArp
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class LaunchArp(ILaunchArp):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def arp(self) -> list[Arp]:
        return self.appliance.arp()
