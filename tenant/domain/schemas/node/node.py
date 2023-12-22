from pydantic import BaseModel
from tenant.domain.schemas.node.connection_protocol import ConnectionProtocol


class Node(BaseModel):
    name: str
    technology: str
    vendor: str
    model: str
    softwareVersion: str
    ipAddress: str
    protocol: ConnectionProtocol
    port: int




