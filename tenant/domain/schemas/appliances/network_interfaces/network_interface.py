from typing import Optional

from pydantic import BaseModel


class NetworkInterface(BaseModel):
    name: str
    description: Optional[str] = ""
    macAddress: str
    ipAddress: Optional[str] = "unassigned"
    mtu: int
    status: str
    protocol: str

    class Config:
        json_schema_extra = {
            "example": [
                {
                    "name": "Ethernet0/0",
                    "description": "",
                    "macAddress": "aabb.cc00.0100",
                    "ipAddress": "unassigned",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet0/1",
                    "description": "",
                    "macAddress": "aabb.cc00.0110",
                    "ipAddress": "unassigned",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet0/2",
                    "description": "",
                    "macAddress": "aabb.cc00.0120",
                    "ipAddress": "unassigned",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet0/3",
                    "description": "",
                    "macAddress": "aabb.cc00.0130",
                    "ipAddress": "unassigned",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet1/0",
                    "description": "",
                    "macAddress": "aabb.cc00.0101",
                    "ipAddress": "unassigned",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet1/1",
                    "description": "",
                    "macAddress": "aabb.cc00.0111",
                    "ipAddress": "unassigned",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet1/2",
                    "description": "",
                    "macAddress": "aabb.cc00.0121",
                    "ipAddress": "unassigned",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet1/3",
                    "description": "",
                    "macAddress": "aabb.cc00.0131",
                    "ipAddress": "unassigned",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet2/0",
                    "description": "",
                    "macAddress": "aabb.cc00.0102",
                    "ipAddress": "unassigned",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet2/1",
                    "description": "",
                    "macAddress": "aabb.cc00.0112",
                    "ipAddress": "unassigned",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet2/2",
                    "description": "",
                    "macAddress": "aabb.cc00.0122",
                    "ipAddress": "unassigned",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet2/3",
                    "description": "",
                    "macAddress": "aabb.cc00.0132",
                    "ipAddress": "unassigned",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet3/0",
                    "description": "",
                    "macAddress": "aabb.cc00.0103",
                    "ipAddress": "unassigned",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet3/1",
                    "description": "",
                    "macAddress": "aabb.cc00.0113",
                    "ipAddress": "unassigned",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet3/2",
                    "description": "",
                    "macAddress": "aabb.cc00.0123",
                    "ipAddress": "unassigned",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Ethernet3/3",
                    "description": "",
                    "macAddress": "aabb.cc00.0133",
                    "ipAddress": "unassigned",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Vlan1",
                    "description": "sw2-uoc-lab",
                    "macAddress": "aabb.cc80.0100",
                    "ipAddress": "192.168.20.10/24",
                    "mtu": 1500,
                    "status": "up",
                    "protocol": "up"
                },
                {
                    "name": "Vlan120",
                    "description": "",
                    "macAddress": "aabb.cc80.0100",
                    "ipAddress": "192.168.90.4/20",
                    "mtu": 1500,
                    "status": "administratively down",
                    "protocol": "down"
                },
                {
                    "name": "Vlan150",
                    "description": "",
                    "macAddress": "aabb.cc80.0100",
                    "ipAddress": "192.168.120.4/20",
                    "mtu": 1500,
                    "status": "down",
                    "protocol": "down"
                }
            ]
        }
