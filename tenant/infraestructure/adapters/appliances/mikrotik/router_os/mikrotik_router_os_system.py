import json

import requests
import urllib3
from requests.auth import HTTPBasicAuth

from tenant.domain.schemas.appliances.system.hostname import Hostname
from tenant.domain.schemas.appliances.system.restart import Restart
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.infraestructure.adapters.appliances.mikrotik.router_os.mikrotik_router_os_save_config import \
    MikrotikRouterOSSaveConfig
from tenant.infraestructure.gateways.appliance.interface_system import ISystem


class MikrotikRouterOSSystem(ISystem):
    def __init__(self, node: NodeWithCredentials):
        self.node = node
        urllib3.disable_warnings()

    def restart(self) -> Restart:
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/system/reboot"
        headers = {"content-type": "application/json"}

        requests.request(method="POST", url=url,
                         auth=HTTPBasicAuth(self.node.username, self.node.password),
                         headers=headers,
                         verify=False)
        r = {
            "status": "ok",
            "message": f"rebooting {self.node.name} device..."
        }
        return Restart(**r)

    def set_hostname(self, new_hostname: str) -> Hostname:
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/system/identity/set"
        headers = {"content-type": "application/json"}
        payload = {"name": new_hostname}

        r = requests.request(method="POST", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers, data=json.dumps(payload),
                             verify=False)

        MikrotikRouterOSSaveConfig(self.node)

        if r.status_code == 200:
            response = {
                "status": "ok",
                "message": f"New hostname {new_hostname}, successfully updated"
            }
        else:
            response = {
                "status": "nok",
                "message": f"ERROR: New hostname {new_hostname}, unsuccessfully updated"
            }

        return Hostname(**response)
