from typing import Optional

from pydantic import BaseModel


class RoundTrip(BaseModel):
    min: Optional[str] = " "
    avg: Optional[str] = " "
    max: Optional[str] = " "
