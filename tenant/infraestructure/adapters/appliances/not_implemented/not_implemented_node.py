from tenant.domain.schemas.appliances.diagnostics.arp import Arp
from tenant.domain.schemas.appliances.diagnostics.ping import Ping
from tenant.domain.schemas.appliances.diagnostics.ping_command_fields import PingCommandFields
from tenant.domain.schemas.appliances.diagnostics.trace_route import TraceRoute
from tenant.domain.schemas.appliances.diagnostics.trace_route_command_fields import TraceRouteCommandFields
from tenant.infraestructure.gateways.appliance.interface_diagnostics import IDiagnostics


class NotImplementedDiagnostics(IDiagnostics):
    def ping(self, ping_command_fields: PingCommandFields) -> Ping:
        pass

    def traceroute(self, trace_route_command_fields: TraceRouteCommandFields) -> TraceRoute:
        pass

    def arp(self) -> Arp:
        pass