import json

import requests
import urllib3
from requests.auth import HTTPBasicAuth

from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.infraestructure.adapters.appliances.mikrotik.router_os.mikrotik_router_os_interfaces import \
    MikrotikRouterOSInterfaces
from tenant.infraestructure.adapters.appliances.mikrotik.router_os.mikrotik_router_os_save_config import \
    MikrotikRouterOSSaveConfig
from tenant.infraestructure.gateways.appliance.interface_svi import ISvi


class MikrotikRouterOSSvi(ISvi):

    def __init__(self, node: NodeWithCredentials):
        self.node = node
        urllib3.disable_warnings()

    def create_svi(self, vlan_id: str) -> NetworkInterface:

        headers = {"content-type": "application/json"}
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/vlan/add"
        payload = {"name": f"vlan{vlan_id}", "vlan-id": vlan_id}

        r = requests.request(method="POST", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers, data=json.dumps(payload),
                             verify=False)
        MikrotikRouterOSSaveConfig(self.node)
        response = MikrotikRouterOSInterfaces(self.node).display(f"vlan{vlan_id}")
        return response[0]

    def set_svi_ip(self, svi: str, ip_address: str) -> NetworkInterface:
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/ip/address/add"
        headers = {"content-type": "application/json"}
        payload = {"interface": f"{svi}", "address": ip_address}

        r = requests.request(method="POST", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers, data=json.dumps(payload),
                             verify=False)
        MikrotikRouterOSSaveConfig(self.node)
        response = MikrotikRouterOSInterfaces(self.node).display(svi)
        return response[0]

    def delete_svi(self, vlan_id: str) -> list[NetworkInterface]:

        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/vlan"
        headers = {"content-type": "application/json"}
        payload = {"name": f"vlan{vlan_id}"}

        r = requests.request(method="GET", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers, data=json.dumps(payload),
                             verify=False)
        line_id = None
        for line in r.json():
            if line["name"] == f"vlan{vlan_id}":
                line_id = line[".id"]
                break

        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/vlan/{line_id}"
        headers = {"content-type": "application/json"}
        payload = {"name": f"vlan{vlan_id}"}

        requests.request(method="DELETE", url=url,
                         auth=HTTPBasicAuth(self.node.username, self.node.password),
                         headers=headers, data=json.dumps(payload),
                         verify=False)

        MikrotikRouterOSSaveConfig(self.node)
        response = MikrotikRouterOSInterfaces(self.node).display()
        return response
