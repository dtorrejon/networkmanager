from netmiko import BaseConnection

from tenant.domain.models.status import Status
from tenant.domain.schemas.appliances.system.hostname import Hostname
from tenant.domain.schemas.appliances.system.restart import Restart
from tenant.infraestructure.gateways.appliance.interface_system import ISystem
from tenant.infraestructure.adapters.appliances.cisco.formatter.system.cisco_ios_restart_fomatter import \
    CiscoIosRestartFormatter


class CiscoIosSystem(ISystem):

    def __init__(self, connect: BaseConnection):
        self.connect: BaseConnection = connect

    def restart(self) -> Restart:
        configuration_register = self.connect.send_command("show version | include Configuration register")
        if "0x2102" not in configuration_register:
            return Restart(
                **{"status": Status.NOK, "message": f"Can't reboot device. {configuration_register}, and must be 0x2102"})
        else:
            self.connect.secret = self.connect.password
            self.connect.enable()
            restart_response = self.connect.send_command("reload")
            if restart_response == f"Proceed with reload? [confirm]":
                self.connect.send_command("\r\n")

            return CiscoIosRestartFormatter().format(restart_response)

    def set_hostname(self, new_hostname: str) -> Hostname:
        self.connect.secret = self.connect.password
        self.connect.enable()
        self.connect.send_command(f"configure terminal",expect_string=r"#")
        self.connect.send_command(f"hostname {new_hostname}", expect_string=r"#")
        self.connect.send_command(f"exit", expect_string=r"#")
        hostname_response: str = self.connect.send_command(f"wr", expect_string=r"#")
        if f"{new_hostname}" in hostname_response:
            return Hostname(status="OK", message=f"New hostname {new_hostname}, successfully updated")
        else:
            return Hostname(status="KO", message=f"Failed to update hostname")