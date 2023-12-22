from typing import Optional

from pydantic import BaseModel


class PingCommandFields(BaseModel):
    sourceIpAddress: Optional[str] = None
    destinationIpAddress: str
    repeat: Optional[int] = 5
