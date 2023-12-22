import json
from typing import Any

import requests
from requests.auth import HTTPBasicAuth

from tenant.domain.models.tcp_service_status import TCPServiceStatus
from tenant.domain.schemas.appliances.commands.command import Command
from tenant.domain.schemas.appliances.commands.script import Script
from tenant.infraestructure.adapters.appliances.mikrotik.router_os.mikrotik_router_os_diagnostics import \
    MikrotikRouterOSDiagnostics
from tenant.infraestructure.adapters.appliances.mikrotik.router_os.mikrotik_router_os_interfaces import \
    MikrotikRouterOSInterfaces
from tenant.infraestructure.adapters.appliances.mikrotik.router_os.mikrotik_router_os_routes import \
    MikrotikRouterOSRoutes
from tenant.infraestructure.adapters.appliances.mikrotik.router_os.mikrotik_router_os_svi import MikrotikRouterOSSvi
from tenant.infraestructure.adapters.appliances.mikrotik.router_os.mikrotik_router_os_system import \
    MikrotikRouterOSSystem
from tenant.infraestructure.adapters.appliances.mikrotik.router_os.mikrotik_router_os_vlan import MikrotikRouterOSVlan
from tenant.infraestructure.adapters.appliances.not_implemented.not_implemented_svi import NotImplementedSvi
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class MikrotikSwitchl3Api(Appliance):

    def __init__(self, node_name: str):
        super().__init__(node_name)
        self.diagnostics = MikrotikRouterOSDiagnostics(self.node)
        self.system = MikrotikRouterOSSystem(self.node)
        self.network_interfaces = MikrotikRouterOSInterfaces(self.node)
        self.routes = MikrotikRouterOSRoutes(self.node)
        # self.svi = NotImplementedSvi()
        self.svi = MikrotikRouterOSSvi(self.node)
        self.vlan = MikrotikRouterOSVlan(self.node)

    def connect(self) -> Any:
        pass

    def send_command(self, command: str) -> Command:
        cmd = command.split(" ")[0]
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest{cmd}"
        parameters_dict = {}

        parameters = command.split(" ")[1:-1]
        for parameter in parameters:
            temp_param = parameter.split("=")
            if len(temp_param) <= 1:
                k = temp_param[0]
                v = "yes"
            elif len(temp_param) == 2:
                k = temp_param[0]
                v = temp_param[1]
            else:
                continue

            parameters_dict.update({f"{k}": f"{v}"})
        print(cmd)
        print(parameters_dict)

        headers = {"content-type": "application/json"}

        r = requests.request(method="POST", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers, data=json.dumps(parameters_dict),
                             verify=False)

        return Command(**{
            "command": f"{command}",
            "response": f"{json.dumps(r.json(), indent=2)}"
        })

    def send_script(self, script: Script) -> list[Command]:
        cmd_list: list[Command] = []
        for cmd in script.model_dump()["commands"]:
            cmd_list.append(self.send_command(cmd))

        return cmd_list



    def service_status(self) -> bool:
        return TCPServiceStatus.status(self.node.ipAddress, self.node.port)
