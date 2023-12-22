from pydantic import BaseModel


class CompatibleNode(BaseModel):
    vendor: str
    model: str
    technology: str
    softwareVersion: str


