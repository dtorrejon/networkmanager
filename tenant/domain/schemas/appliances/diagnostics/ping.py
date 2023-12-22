from typing import Optional

from pydantic import BaseModel

from tenant.domain.schemas.appliances.diagnostics.round_trip import RoundTrip


class Ping(BaseModel):
    source: str
    destination: str
    packetsTransmitted: Optional[int] = 0
    packetsReceived: Optional[int] = 0
    percent: Optional[str] = "0%"
    roundTrip: Optional[RoundTrip]

    class Config:
        json_schema_extra = {
            "example": {
                "source": "192.168.20.10",
                "destination": "8.8.8.8",
                "packetsTransmitted": 4,
                "packetsReceived": 4,
                "percent": "100%",
                "roundTrip": {
                    "min": "26 ms",
                    "avg": "38 ms",
                    "max": "51 ms"
                }
            }
        }
