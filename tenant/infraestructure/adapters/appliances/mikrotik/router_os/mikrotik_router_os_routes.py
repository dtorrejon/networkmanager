import json

import requests
import urllib3
from requests.auth import HTTPBasicAuth

from tenant.domain.models.mikrotik_route_codes import MikrotikRouteCodes
from tenant.domain.schemas.appliances.diagnostics.route import Route
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.infraestructure.adapters.appliances.mikrotik.router_os.mikrotik_router_os_save_config import \
    MikrotikRouterOSSaveConfig
from tenant.infraestructure.gateways.appliance.interface_routes import IRoutes


class MikrotikRouterOSRoutes(IRoutes):
    def __init__(self, node: NodeWithCredentials):
        self.node = node
        urllib3.disable_warnings()

    def routing_table(self) -> list[Route]:
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/ip/route"
        headers = {"content-type": "application/json"}

        response = requests.request(method="GET", url=url,
                                    auth=HTTPBasicAuth(self.node.username, self.node.password),
                                    headers=headers,
                                    verify=False)

        route_output_list: list[Route] = []
        id: int = 0
        for line in response.json():
            try:
                interface = line["local-address"]
            except:
                interface = "-"
            id += 1
            route = {
                "id": id,
                "destination": line["dst-address"],
                "protocol": self._check_route_protocols(**line),
                "preference": line["scope"],
                "cost": line["distance"],
                "nextHop": self._get_interface(**line),
                "interface": line["gateway"],
                "age": "-"
            }
            route_output_list.append(Route(**route))

        return route_output_list

    def set_default_gateway(self, ip: str) -> list[Route]:
        return self.set_static_route("0.0.0.0/0", ip)

    def set_static_route(self, ip_and_mask_in_cidr: str, ip_next_hop: str) -> list[Route]:
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/ip/route/add"
        headers = {"content-type": "application/json"}
        payload = {"dst-address": f"{ip_and_mask_in_cidr}", "gateway": f"{ip_next_hop}"}

        r = requests.request(method="POST", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers, data=json.dumps(payload),
                             verify=False)
        MikrotikRouterOSSaveConfig(self.node)

        return self.routing_table()

    @staticmethod
    def _check_route_protocols(**kwargs) -> str:
        response_list: list[str] = []
        for k, v in kwargs.items():
            if k.lower() in MikrotikRouteCodes.get_names_in_a_string().lower():
                if v == "true":
                    response_list.append(k)
        return " ".join(response_list)

    @staticmethod
    def _get_interface(**kwargs) -> str:
        response = "-"
        for k, v in kwargs.items():
            if k == "local-address" or k == "immediate-gw":
                response = v

        return response
