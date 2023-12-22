from typing import Optional

from pydantic import BaseModel


class Route(BaseModel):
    id: int
    destination: Optional[str]
    protocol: Optional[str]
    preference: Optional[int]
    cost: Optional[int]
    nextHop: Optional[str]
    interface: Optional[str]
    age: Optional[str]
