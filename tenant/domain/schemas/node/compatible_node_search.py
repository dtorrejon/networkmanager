from typing import Optional

from pydantic import BaseModel


class CompatibleNodeSearch(BaseModel):
    vendor: Optional[str] = None
    model: Optional[str] = None
    technology: Optional[str] = None
    softwareVersion: Optional[str] = None
