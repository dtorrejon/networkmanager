from typing import Any
from tenant.domain.schemas.node.connection_protocol import ConnectionProtocolDefaultPort
from tenant.domain.schemas.node.node import Node


class NewNode(Node):
    port: int | None = 0
    username: str
    password: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.port is None or self.port == 0:
            self.port = ConnectionProtocolDefaultPort[self.protocol.value.upper()].value
