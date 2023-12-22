from typing import Optional

from pydantic import BaseModel


class NetworkInterfaceBrief(BaseModel):
    name: str
    ipAddress: Optional[str] = "unassigned"
    status: str
    protocol: str

    class Config:
        json_schema_extra = {
            "example": [
                {
                    "name": "Ethernet0/0",
                    "ipAddress": "unassigned",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet0/1",
                    "ipAddress": "unassigned",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet0/2",
                    "ipAddress": "unassigned",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet0/3",
                    "ipAddress": "unassigned",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet1/0",
                    "ipAddress": "unassigned",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet1/1",
                    "ipAddress": "unassigned",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet1/2",
                    "ipAddress": "unassigned",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet1/3",
                    "ipAddress": "unassigned",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet2/0",
                    "ipAddress": "unassigned",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet2/1",
                    "ipAddress": "unassigned",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet2/2",
                    "ipAddress": "unassigned",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet2/3",
                    "ipAddress": "unassigned",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet3/0",
                    "ipAddress": "unassigned",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet3/1",
                    "ipAddress": "unassigned",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet3/2",
                    "ipAddress": "unassigned",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet3/3",
                    "ipAddress": "unassigned",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Vlan1",
                    "ipAddress": "192.168.20.10",
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Vlan120",
                    "ipAddress": "192.168.90.4",
                    "status": "administratively down",
                    "protocol": "down"
                },
                {
                    "name": "Vlan150",
                    "ipAddress": "192.168.120.4",
                    "status": "down",
                    "protocol": "down"
                }
            ]
        }
