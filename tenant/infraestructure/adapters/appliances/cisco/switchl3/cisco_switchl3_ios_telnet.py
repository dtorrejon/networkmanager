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


class CiscoSwitchl3IosTelnet(Appliance):
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
        return ConnectHandler(device_type="cisco_ios_telnet", ip=self.node.ipAddress,
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


if __name__ == '__main__':
    # print("Test PING")

    tn = CiscoSwitchl3IosTelnet("sw01")
    # tn.display()
    # tn.display_brief()
    # print(tn.send_command("sh ip interface brief"))
    # ping_command_fields = PingCommandFields(sourceIpAddress = "192.168.20.10", repeat=100, destinationIpAddress = "8.8.4.4")
    # ping = tn.diagnostics.ping(ping_command_fields)
    # print(json.dumps(ping.model_dump(), indent=4))

    # arp = tn.arp()
    # print(json.dumps(arp.model_dump(), indent=4))
    # restart = tn.diagnostics.restart()
    # print(restart)

    # tr = TraceRouteCommandFields(destinationIpAddress="1.1.1.1", probeCount=6)
    # t = tn.diagnostics.traceroute(tr)
    # print(json.dumps(t.model_dump(), indent=5))

    # rt = tn.arp()
    # print(json.dumps(rt.model_dump(), indent=2))

    tn.display_vlan_brief()
