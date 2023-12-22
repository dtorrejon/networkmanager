from tenant.domain.schemas.appliances.commands.command import Command
from tenant.domain.schemas.appliances.commands.script import Script
from tenant.domain.models.tcp_service_status import TCPServiceStatus
from tenant.infraestructure.adapters.appliances.cisco.ios.cisco_ios_svi import CiscoIosSvi
from tenant.infraestructure.adapters.appliances.cisco.ios.cisco_ios_vlan import CiscoIosVlan
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance
from netmiko import ConnectHandler, BaseConnection
from tenant.infraestructure.adapters.appliances.cisco.ios.cisco_ios_diagnotics import \
    CiscoIosDiagnostics
from tenant.infraestructure.adapters.appliances.cisco.ios.cisco_ios_network_interfaces import \
    CiscoIosNetworkInterfaces
from tenant.infraestructure.adapters.appliances.cisco.ios.cisco_ios_routes import \
    CiscoIosStaticRoutes
from tenant.infraestructure.adapters.appliances.cisco.ios.cisco_ios_system import \
    CiscoIosSystem


class CiscoSwitchl3IosSsh(Appliance):
    def __init__(self, node_name: str):
        super().__init__(node_name)
        self.connection: BaseConnection = self.connect
        self.diagnostics = CiscoIosDiagnostics(self.connection)
        self.system = CiscoIosSystem(self.connection)
        self.network_interfaces = CiscoIosNetworkInterfaces(self.connection)
        self.routes = CiscoIosStaticRoutes(self.connection)
        self.svi = CiscoIosSvi(self.connection)
        self.vlan = CiscoIosVlan(self.connection)

    @property
    def connect(self) -> BaseConnection:
        return ConnectHandler(device_type="cisco_ios", ip=self.node.ipAddress,
                              username=self.node.username, password=self.node.password,
                              fast_cli=True)

    def send_command(self, command: str) -> Command:
        response = self.connect.send_command_timing(command)
        output: dict = {"command": f"{command}", "response": f"{response}"}
        return Command(**output)

    def send_script(self, script: Script) -> list[Command]:
        commands: list[Command] = []
        for cmd in script.model_dump()["commands"]:
            commands.append(self.send_command(cmd))
        return commands

    def service_status(self) -> bool:
        return TCPServiceStatus.status(self.node.ipAddress, self.node.port)