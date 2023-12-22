from typing import Optional

from pydantic import BaseModel


class TraceRouteProbeCount(BaseModel):
    id: Optional[str]
    ip: Optional[str]
    time: Optional[str]
    timeScale: Optional[str]
