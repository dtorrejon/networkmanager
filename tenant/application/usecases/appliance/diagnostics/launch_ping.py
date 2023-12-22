
from tenant.domain.ports.appliances.diagnostics.interface_launch_ping import ILaunchPing
from tenant.domain.schemas.appliances.diagnostics.ping import Ping
from tenant.domain.schemas.appliances.diagnostics.ping_command_fields import PingCommandFields
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class LaunchPing(ILaunchPing):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def ping(self, ping_command_fields: PingCommandFields) -> Ping:
        return self.appliance.ping(ping_command_fields)
