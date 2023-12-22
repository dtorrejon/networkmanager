from pydantic import BaseModel

from tenant.domain.schemas.node.connection_protocol import ConnectionProtocol


class ExistingNode(BaseModel):
    name: str | None = ""
    newName: str | None = ""
    vendor: str | None = ""
    technology: str | None = ""
    model: str | None = ""
    softwareVersion: str | None = ""
    ipAddress: str | None = ""
    protocol: ConnectionProtocol | None = ""
    port: int | None = -1
    username: str | None = ""
    password: str | None = ""
