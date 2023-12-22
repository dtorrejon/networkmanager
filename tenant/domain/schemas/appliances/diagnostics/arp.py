from typing import Optional

from pydantic import BaseModel


class Arp(BaseModel):
    protocol: Optional[str] = ""
    ipAddress: Optional[str] = ""
    macAddress: Optional[str] = ""
    age: Optional[str] = -1
    type: Optional[str] = ""
    interface: Optional[str] = ""

    class Config:
        json_schema_extra = {
            "example": [
                {
                    "protocol": "Internet",
                    "ipAddress": "192.168.20.1",
                    "macAddress": "0c68.b791.0002",
                    "age": "5",
                    "type": "ARPA",
                    "interface": "Vlan1"
                },
                {
                    "protocol": "Internet",
                    "ipAddress": "192.168.20.10",
                    "macAddress": "aabb.cc80.0100",
                    "age": "-",
                    "type": "ARPA",
                    "interface": "Vlan1"
                },
                {
                    "protocol": "Internet",
                    "ipAddress": "192.168.120.4",
                    "macAddress": "aabb.cc80.0100",
                    "age": "-",
                    "type": "ARPA",
                    "interface": "Vlan150"
                }
            ]
        }
