from abc import ABCMeta, abstractmethod
from tenant.domain.schemas.appliances.diagnostics.arp import Arp
from tenant.domain.schemas.appliances.diagnostics.ping import Ping
from tenant.domain.schemas.appliances.diagnostics.ping_command_fields import PingCommandFields
from tenant.domain.schemas.appliances.diagnostics.trace_route import TraceRoute
from tenant.domain.schemas.appliances.diagnostics.trace_route_command_fields import TraceRouteCommandFields


class IDiagnostics(metaclass=ABCMeta):

    @abstractmethod
    def ping(self, ping_command_fields: PingCommandFields) -> Ping:
        ...

    @abstractmethod
    def traceroute(self, trace_route_command_fields: TraceRouteCommandFields) -> TraceRoute:
        ...

    @abstractmethod
    def arp(self) -> list[Arp]:
        ...

