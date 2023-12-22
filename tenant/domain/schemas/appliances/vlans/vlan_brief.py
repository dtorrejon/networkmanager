from typing import Optional

from pydantic import BaseModel


class VlanBrief(BaseModel):
    vlan: int
    name: str
    status: str
    ports: Optional[list[str]] = ""

