from tenant.domain.schemas.appliances.commands.command import Command
from tenant.domain.schemas.appliances.commands.script import Script
from tenant.domain.ports.appliances.commands.interface_send_script import ISendScript
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class SendScript(ISendScript):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def send_script(self, script: Script) -> list[Command]:
        return self.appliance.send_script(script)
