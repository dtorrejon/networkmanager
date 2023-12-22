from tenant.domain.models.status import Status
from tenant.domain.schemas.appliances.system.restart import Restart
from tenant.infraestructure.gateways.appliance.formatter.system.interface_restart_formatter import IRestartFormatter


class CiscoIosRestartFormatter(IRestartFormatter):
    def format(self, restart_text: str) -> Restart:
        if restart_text == f"Proceed with reload? [confirm]":

            return Restart(**{"status": Status.OK, "message": f"Rebooting device..."})
        else:
            return Restart(**{"status": Status.NOK, "message": f"Can't reboot device."})