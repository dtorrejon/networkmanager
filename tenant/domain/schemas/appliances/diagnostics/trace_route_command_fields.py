from typing import Optional

from pydantic import BaseModel


class TraceRouteCommandFields(BaseModel):
    protocol: Optional[str] = "ip"
    sourceIpAddress: Optional[str] = None
    destinationIpAddress: str
    timeout: Optional[int] = 3
    probeCount: Optional[int] = 3
    minimumTTL: Optional[int] = 1
    maximumTTL: Optional[int] = 30
