
from tenant.domain.ports.appliances.system.interface_launch_restart import ILaunchRestart
from tenant.domain.schemas.appliances.system.restart import Restart
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class LaunchRestart(ILaunchRestart):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def restart(self) -> Restart:
        return self.appliance.restart()