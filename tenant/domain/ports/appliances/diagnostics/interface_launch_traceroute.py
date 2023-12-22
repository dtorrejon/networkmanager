from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.diagnostics.trace_route import TraceRoute
from tenant.domain.schemas.appliances.diagnostics.trace_route_command_fields import TraceRouteCommandFields


class ILaunchTraceRoute(metaclass=ABCMeta):

    @abstractmethod
    def trace_route(self, trace_route_command_fields: TraceRouteCommandFields) -> TraceRoute:
        ...