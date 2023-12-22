import json
from typing import Optional
import urllib3
import requests
from requests.auth import HTTPBasicAuth

from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.domain.schemas.appliances.network_interfaces.network_interface_brief import NetworkInterfaceBrief
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.infraestructure.adapters.appliances.mikrotik.router_os.mikrotik_router_os_save_config import \
    MikrotikRouterOSSaveConfig
from tenant.infraestructure.gateways.appliance.interface_network_interfaces import INetworkInterfaces


class MikrotikRouterOSInterfaces(INetworkInterfaces):

    def __init__(self, node: NodeWithCredentials):
        self.node = node
        urllib3.disable_warnings()

    def display(self, interface: Optional[str] = None) -> list[NetworkInterface]:
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface"
        headers = {"content-type": "application/json"}

        response = requests.request(method="GET", url=url,
                                    auth=HTTPBasicAuth(self.node.username, self.node.password),
                                    headers=headers,
                                    verify=False)
        interfaces_response = response.json()
        if interface is not None:
            for line in interfaces_response:
                if line["name"] == interface:
                    interfaces_response = [line]
                    break
        print(response.json())
        output = []
        for line in interfaces_response:

            if line["disabled"] == "false":
                status = "up"
            else:
                status = "down"

            if line["running"] == "true":
                protocol = "up"
            else:
                protocol = "down"

            try:
                comment = line["comment"]
            except:
                comment = ""

            if line["mtu"] != "auto":
                mtu = line["mtu"]
            else:
                mtu = line["actual-mtu"]
            ip_addr = self._get_ip(line["name"])
            interface_line = {
                "name": line["name"],
                "description": comment,
                "macAddress": line["mac-address"],
                "ipAddress": ip_addr ,
                "mtu": mtu,
                "status": status,
                "protocol": protocol
            }
            output.append(NetworkInterface(**interface_line))

        return output

    def display_interface_brief(self) -> list[NetworkInterfaceBrief]:
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface"
        headers = {"content-type": "application/json"}

        response = requests.request(method="GET", url=url,
                                    auth=HTTPBasicAuth(self.node.username, self.node.password),
                                    headers=headers,
                                    verify=False)
        interfaces_response = response.json()

        output = []
        for line in interfaces_response:

            if line["disabled"] == "false":
                status = "up"
            else:
                status = "down"

            if line["running"] == "true":
                protocol = "up"
            else:
                protocol = "down"

            interface_line = {
                "ipAddress": self._get_ip(line["name"]),
                "name": line["name"],
                "protocol": protocol,
                "status": status
            }
            output.append(NetworkInterfaceBrief(**interface_line))

        return output

    def no_shutdown(self, interface: str) -> NetworkInterface:
        return self._set_shutdown(interface, "no")

    def shutdown(self, interface: str) -> NetworkInterface:
        return self._set_shutdown(interface, "yes")

    def set_ip(self, interface: str, ip_address_and_mask: str) -> NetworkInterface:
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/ip/address/add"
        headers = {"content-type": "application/json"}
        payload = {"interface": f"{interface}", "address": f"{ip_address_and_mask}"}

        requests.request(method="POST", url=url,
                         auth=HTTPBasicAuth(self.node.username, self.node.password),
                         headers=headers, data=json.dumps(payload),
                         verify=False)

        MikrotikRouterOSSaveConfig(self.node)
        return self.display(interface)[0]

    def set_description(self, interface: str, description: str) -> NetworkInterface:
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/ethernet/{self._get_interface_info(interface)[0]['.id']}"
        headers = {"content-type": "application/json"}
        payload = {"comment": f"{description}"}

        requests.request(method="PATCH", url=url,
                         auth=HTTPBasicAuth(self.node.username, self.node.password),
                         headers=headers, data=json.dumps(payload),
                         verify=False)
        MikrotikRouterOSSaveConfig(self.node)
        return self.display(interface)[0]

    def _get_ip(self, interface: str)-> str:

        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/ip/address"
        headers = {"content-type": "application/json"}
        ip_response = requests.request(method="GET", url=url,
                                       auth=HTTPBasicAuth(self.node.username, self.node.password),
                                       headers=headers,
                                       verify=False)
        ip = "unassigned"
        print(ip_response.json())
        for line in ip_response.json():
            if line["interface"] == interface:
                return line["address"]

        return ip

    def _set_shutdown(self, interface: str, disabled: str) -> NetworkInterface:

        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/ethernet/{self._get_interface_info(interface)[0]['.id']}"
        headers = {"content-type": "application/json"}
        payload = {"disabled": f"{disabled}"}

        requests.request(method="PATCH", url=url,
                         auth=HTTPBasicAuth(self.node.username, self.node.password),
                         headers=headers, data=json.dumps(payload),
                         verify=False)

        MikrotikRouterOSSaveConfig(self.node)

        return self.display(interface)[0]

    def _get_interface_info(self, interface: str) -> list:
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface"
        headers = {"content-type": "application/json"}

        response = requests.request(method="GET", url=url,
                                    auth=HTTPBasicAuth(self.node.username, self.node.password),
                                    headers=headers,
                                    verify=False)
        interfaces_response = response.json()

        if interface is not None:
            for line in interfaces_response:
                if line["name"] == interface:
                    interfaces_response = [line]
                    return interfaces_response

        return []
