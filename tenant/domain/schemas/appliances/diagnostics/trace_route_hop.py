from typing import Optional

from pydantic import BaseModel

from tenant.domain.schemas.appliances.diagnostics.trace_route_probe_count import TraceRouteProbeCount


class TraceRouteHop(BaseModel):
    hopNumber: Optional[str]
    probeCount: Optional[list[TraceRouteProbeCount]]
