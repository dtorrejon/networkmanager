from tenant.domain.schemas.appliances.diagnostics.arp import Arp
from tenant.domain.schemas.appliances.diagnostics.ping import Ping
from tenant.domain.schemas.appliances.diagnostics.ping_command_fields import PingCommandFields
from tenant.domain.schemas.appliances.diagnostics.trace_route import TraceRoute
from tenant.domain.schemas.appliances.diagnostics.trace_route_command_fields import TraceRouteCommandFields
from tenant.infraestructure.gateways.appliance.interface_diagnostics import IDiagnostics
from netmiko import BaseConnection
import pexpect

from tenant.infraestructure.adapters.appliances.cisco.formatter.diagnostics.cisco_ios_arp_formatter import \
    CiscoIosArpFormatter
from tenant.infraestructure.adapters.appliances.cisco.formatter.diagnostics.cisco_ios_traceroute_formatter import \
    CiscoIosTraceRouteFormatter
from tenant.infraestructure.adapters.appliances.cisco.formatter.diagnostics.cisco_ios_ping_formatter import \
    CiscoIosPingFormatter


class CiscoIosDiagnostics(IDiagnostics):

    def __init__(self, connect: BaseConnection):
        self.connect: BaseConnection = connect

    def traceroute(self, trace_route_command_fields: TraceRouteCommandFields) -> TraceRoute:

        if trace_route_command_fields.sourceIpAddress is None:
            trace_route_command_fields.sourceIpAddress = self.connect.host

        self.connect.secret = self.connect.password
        self.connect.enable()
        self.connect.find_prompt()
        self.connect.send_command_timing("traceroute", strip_command=False, strip_prompt=False)
        self.connect.send_command_timing(f"{trace_route_command_fields.protocol}", strip_command=False,
                                         strip_prompt=False)
        self.connect.send_command_timing(f"{trace_route_command_fields.destinationIpAddress}", strip_command=False,
                                         strip_prompt=False)
        self.connect.send_command_timing(f"{trace_route_command_fields.sourceIpAddress}", strip_command=False,
                                         strip_prompt=False)
        self.connect.send_command_timing(f"n", strip_command=False, strip_prompt=False)
        self.connect.send_command_timing(f"{trace_route_command_fields.timeout}", strip_command=False,
                                         strip_prompt=False)
        self.connect.send_command_timing(f"{trace_route_command_fields.probeCount}", strip_command=False,
                                         strip_prompt=False)
        self.connect.send_command_timing(f"{trace_route_command_fields.minimumTTL}", strip_command=False,
                                         strip_prompt=False)
        self.connect.send_command_timing(f"{trace_route_command_fields.maximumTTL}", strip_command=False,
                                         strip_prompt=False)
        self.connect.send_command_timing(f"33434", strip_command=False, strip_prompt=False)
        response = self.connect.send_command_timing(f"", strip_command=False, strip_prompt=False, last_read=30,
                                                    read_timeout=120)
        return CiscoIosTraceRouteFormatter().format(response, trace_route_command_fields)

    def ping(self, ping_command_fields: PingCommandFields) -> Ping:
        if ping_command_fields.sourceIpAddress is None:
            ping_command_fields.sourceIpAddress = self.connect.host

        child = pexpect.spawn(f"telnet {self.connect.host} {self.connect.port}")
        child.sendline(f"{self.connect.password}")
        child.expect("Password: ")
        child.sendline(f"en")
        child.expect(f":")
        child.sendline(f"{self.connect.password}")
        child.expect(f"#")
        child.sendline(
            f"ping {ping_command_fields.destinationIpAddress}  source {ping_command_fields.sourceIpAddress} repeat {ping_command_fields.repeat}")
        child.expect(f"#")
        ping_response = child.before.decode("utf-8")
        return CiscoIosPingFormatter().format(ping_command_fields.sourceIpAddress,
                                              ping_command_fields.destinationIpAddress, ping_response)

    def arp(self) -> list[Arp]:
        self.connect.find_prompt()
        self.connect.secret = self.connect.password
        self.connect.enable()
        self.connect.find_prompt()
        arp_response = self.connect.send_command("show arp")

        return CiscoIosArpFormatter().format(arp_response)


