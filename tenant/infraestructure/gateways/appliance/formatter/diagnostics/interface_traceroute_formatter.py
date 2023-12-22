from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.diagnostics.trace_route import TraceRoute
from tenant.domain.schemas.appliances.diagnostics.trace_route_command_fields import TraceRouteCommandFields


class ITraceRouteFormatter(metaclass=ABCMeta):

    @abstractmethod
    def format(self, traceroute_text: str, trace_route_command_fields: TraceRouteCommandFields) -> TraceRoute:
        ...
