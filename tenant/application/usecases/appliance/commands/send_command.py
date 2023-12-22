
from tenant.domain.ports.appliances.commands.interface_send_command import ISendCommand
from tenant.domain.schemas.appliances.commands.command import Command
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class SendCommand(ISendCommand):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def send_command(self, command: str) -> Command:
        return self.appliance.send_command(command)
