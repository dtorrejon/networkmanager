from typing import Optional

from pydantic import BaseModel


class VlanTrunk(BaseModel):
    port: str
    mode: str
    encapsulation: str
    status: str
    nativeVlan: int
    allowedTrunkVlans: list[int] | None = None
