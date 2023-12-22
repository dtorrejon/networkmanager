from tenant.domain.schemas.appliances.diagnostics.trace_route import TraceRoute
from tenant.domain.schemas.appliances.diagnostics.trace_route_command_fields import TraceRouteCommandFields
from tenant.domain.ports.appliances.diagnostics.interface_launch_traceroute import ILaunchTraceRoute
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class LaunchTraceRoute(ILaunchTraceRoute):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def trace_route(self, trace_route_command_fields: TraceRouteCommandFields) -> TraceRoute:
        return self.appliance.trace_route(trace_route_command_fields)
