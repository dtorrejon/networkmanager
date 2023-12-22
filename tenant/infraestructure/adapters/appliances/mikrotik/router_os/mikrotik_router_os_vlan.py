import json
from typing import Union

import requests
import urllib3
from requests.auth import HTTPBasicAuth

from tenant.domain.schemas.appliances.vlans.vlan_brief import VlanBrief
from tenant.domain.schemas.appliances.vlans.vlan_resume import VlanResume
from tenant.domain.schemas.appliances.vlans.vlan_trunk import VlanTrunk
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.infraestructure.adapters.appliances.mikrotik.router_os.mikrotik_router_os_save_config import \
    MikrotikRouterOSSaveConfig
from tenant.infraestructure.gateways.appliance.interface_vlan import IVlan


class MikrotikRouterOSVlan(IVlan):

    def __init__(self, node: NodeWithCredentials):
        self.node = node
        urllib3.disable_warnings()

    def display_vlan_brief(self) -> list[VlanBrief]:
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan"
        headers = {"content-type": "application/json"}

        response_vlan_bridge = requests.request(method="GET", url=url,
                                                auth=HTTPBasicAuth(self.node.username, self.node.password),
                                                headers=headers,
                                                verify=False)

        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/vlan"
        headers = {"content-type": "application/json"}

        response_vlan = requests.request(method="GET", url=url,
                                         auth=HTTPBasicAuth(self.node.username, self.node.password),
                                         headers=headers,
                                         verify=False)

        output_brief = []
        for line in response_vlan_bridge.json():
            status = ""
            if line["disabled"] == "false":
                status = "up"
            elif line["disabled"] == "true":
                status = "down"
            if line["untagged"] == "":
                ports = []
            else:
                ports = str(line["untagged"]).split(",")
            element = {
                "vlan": line["vlan-ids"],
                "name": line["bridge"],
                "status": status,
                "ports": ports
            }
            output_brief.append(VlanBrief(**element))

        for line in response_vlan.json():
            status = ""
            if line["disabled"] == "false":
                status = "up"
            elif line["disabled"] == "true":
                status = "down"
            if line["interface"] == "":
                ports = []
            else:
                ports = str(line["interface"]).split(",")
            element = {
                "vlan": line["vlan-id"],
                "name": line["name"],
                "status": status,
                "ports": ports
            }
            output_brief.append(VlanBrief(**element))
        return output_brief

    def set_vlan_access(self, interface: str, vlan_id: int, bridge: str) -> list[VlanBrief]:
        br = self._check_vlan_bridge_and_create_if_not_exist(bridge)
        self.vlan_filtering(bridge, "off")
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/port"
        headers = {"content-type": "application/json"}

        r = requests.request(method="GET", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers,
                             verify=False)

        port_in_json = False
        for line in r.json():
            if line["interface"] == interface:
                port_in_json = True
                break

        if port_in_json is False:
            url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/port/add"
            headers = {"content-type": "application/json"}
            payload = {"bridge": br, "interface": f"{interface}"}

            requests.request(method="POST", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers, data=json.dumps(payload),
                             verify=False)

            url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan/add"
            headers = {"content-type": "application/json"}
            payload = {"bridge": br, "tagged": br, "untagged": f"{interface}", "vlan-ids": vlan_id}

            requests.request(method="POST", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers, data=json.dumps(payload),
                             verify=False)
            self.vlan_filtering(bridge, "on")
            return self.display_vlan_brief()

        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan"
        headers = {"content-type": "application/json"}

        r = requests.request(method="GET", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers,
                             verify=False)

        vlan_id_exist = False
        for line in r.json():
            if line["vlan-ids"] == vlan_id:
                vlan_id_exist = True

        if port_in_json is True or vlan_id_exist:
            url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan"
            headers = {"content-type": "application/json"}

            r = requests.request(method="GET", url=url,
                                 auth=HTTPBasicAuth(self.node.username, self.node.password),
                                 headers=headers,
                                 verify=False)

            vlan_exist = False
            number_id = None
            untagged = ""
            for line in r.json():
                if int(line["vlan-ids"]) == vlan_id:
                    vlan_exist = True
                    number_id = line[".id"]
                    if line['untagged'] != "" and interface not in line['untagged']:
                        untagged = f"{line['untagged']},{interface}"
                    else:
                        untagged = interface
                    if line["tagged"] == interface:
                        vlan_number_id = line[".id"]
                        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan/{vlan_number_id}"
                        headers = {"content-type": "application/json"}
                        payload = {"tagged": "", ".id": f"{vlan_number_id}"}

                        requests.request(method="PATCH", url=url,
                                         auth=HTTPBasicAuth(self.node.username, self.node.password),
                                         headers=headers, data=json.dumps(payload),
                                         verify=False)

                    if interface in line["tagged"]:
                        vlan_number_id = line[".id"]
                        output_interface_list = []
                        interfaces_in_list = str(line["tagged"]).split(",")
                        for element in interfaces_in_list:
                            if element != interface:
                                output_interface_list.append(element)

                        output_interface_string = ",".join(output_interface_list)
                        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan/{vlan_number_id}"
                        headers = {"content-type": "application/json"}
                        payload = {"tagged": f"{output_interface_string}", ".id": f"{vlan_number_id}"}

                        requests.request(method="PATCH", url=url,
                                         auth=HTTPBasicAuth(self.node.username, self.node.password),
                                         headers=headers, data=json.dumps(payload),
                                         verify=False)

                    break
            """
            for line in r.json():
                if line["untagged"] == interface:
                    vlan_number_id = line[".id"]
                    url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan/{vlan_number_id}"
                    headers = {"content-type": "application/json"}
                    payload = {"untagged": "", ".id": f"{vlan_number_id}"}

                    requests.request(method="PATCH", url=url,
                                     auth=HTTPBasicAuth(self.node.username, self.node.password),
                                     headers=headers, data=json.dumps(payload),
                                     verify=False)

                if interface in line["untagged"]:
                    vlan_number_id = line[".id"]
                    output_interface_list = []
                    interfaces_in_list = str(line["untagged"]).split(",")
                    for element in interfaces_in_list:
                        if element != interface:
                            output_interface_list.append(element)

                    output_interface_string = ",".join(output_interface_list)
                    url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan/{vlan_number_id}"
                    headers = {"content-type": "application/json"}
                    payload = {"untagged": f"{output_interface_string}", ".id": f"{vlan_number_id}"}

                    requests.request(method="PATCH", url=url,
                                     auth=HTTPBasicAuth(self.node.username, self.node.password),
                                     headers=headers, data=json.dumps(payload),
                                     verify=False)
                """
            if vlan_exist:

                url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan/{number_id}"
                headers = {"content-type": "application/json"}
                payload = {"untagged": f"{untagged}", ".id": f"{number_id}"}

                requests.request(method="PATCH", url=url,
                                 auth=HTTPBasicAuth(self.node.username, self.node.password),
                                 headers=headers, data=json.dumps(payload),
                                 verify=False)

            else:

                url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan/add"
                headers = {"content-type": "application/json"}
                payload = {"bridge": br, "tagged": br, "untagged": f"{interface}", "vlan-ids": vlan_id}

                requests.request(method="POST", url=url,
                                 auth=HTTPBasicAuth(self.node.username, self.node.password),
                                 headers=headers, data=json.dumps(payload),
                                 verify=False)

        MikrotikRouterOSSaveConfig(self.node)
        self.vlan_filtering(bridge, "on")
        return self.display_vlan_brief()

    def set_vlan_native(self, interface: str, vlan_id: int, bridge: str) -> list[VlanTrunk]:
        br = self._check_vlan_bridge_and_create_if_not_exist(bridge)
        self.vlan_filtering(bridge, "off")
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/port"
        headers = {"content-type": "application/json"}

        r = requests.request(method="GET", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers,
                             verify=False)

        port_in_json = False
        line_id = None
        for line in r.json():
            if line["interface"] == interface:
                port_in_json = True
                line_id = line[".id"]
                break

        if port_in_json is False:
            url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/port/add"
            headers = {"content-type": "application/json"}
            payload = {"bridge": br, "interface": f"{interface}", "pvid": f"{vlan_id}"}

            requests.request(method="POST", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers, data=json.dumps(payload),
                             verify=False)
        else:
            url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/port/{line_id}"
            headers = {"content-type": "application/json"}
            payload = {".id": line_id, "pvid": f"{vlan_id}"}

            requests.request(method="PATCH", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers, data=json.dumps(payload),
                             verify=False)

        self.set_vlan_access(interface, vlan_id, bridge)
        self.vlan_filtering(bridge, "on")
        return self.display_vlan_trunk()

    def set_vlan_trunk(self, interface: str, vlan_id: list[int], bridge: str) -> list[VlanTrunk]:
        self.vlan_filtering(bridge, "off")
        for vlan in vlan_id:
            self.set_vlan_trunk_by_vlan(interface, vlan, bridge)

        MikrotikRouterOSSaveConfig(self.node)
        self.vlan_filtering(bridge, "on")
        return self.display_vlan_trunk()

    def set_vlan_trunk_by_vlan(self, interface: str, vlan_id: int, bridge: str):
        br = self._check_vlan_bridge_and_create_if_not_exist(bridge)
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/port"
        headers = {"content-type": "application/json"}

        r = requests.request(method="GET", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers,
                             verify=False)


        port_in_json = False
        for line in r.json():
            if line["interface"] == interface:
                port_in_json = True
                break

        if port_in_json is False:
            url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/port/add"
            headers = {"content-type": "application/json"}
            payload = {"bridge": br, "interface": f"{interface}"}

            requests.request(method="POST", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers, data=json.dumps(payload),
                             verify=False)

            url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan/add"
            headers = {"content-type": "application/json"}
            payload = {"bridge": br, "tagged": f"{interface}", "vlan-ids": vlan_id}

            requests.request(method="POST", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers, data=json.dumps(payload),
                             verify=False)

            return

        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan"
        headers = {"content-type": "application/json"}

        r = requests.request(method="GET", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers,
                             verify=False)

        vlan_id_exist = False
        for line in r.json():
            if line["vlan-ids"] == vlan_id:
                vlan_id_exist = True

        if port_in_json is True or vlan_id_exist:
            url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan"
            headers = {"content-type": "application/json"}

            r = requests.request(method="GET", url=url,
                                 auth=HTTPBasicAuth(self.node.username, self.node.password),
                                 headers=headers,
                                 verify=False)

            vlan_exist = False
            number_id = None
            untagged = ""
            tagged = ""
            for line in r.json():
                if int(line["vlan-ids"]) == vlan_id:
                    vlan_exist = True
                    number_id = line[".id"]
                    if line['tagged'] != "" and interface not in line['tagged']:
                        tagged = f"{line['tagged']},{interface}"
                    else:
                        tagged = interface
                    if line["untagged"] == interface:
                        vlan_number_id = line[".id"]
                        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan/{vlan_number_id}"
                        headers = {"content-type": "application/json"}
                        payload = {"untagged": "", ".id": f"{vlan_number_id}"}

                        requests.request(method="PATCH", url=url,
                                         auth=HTTPBasicAuth(self.node.username, self.node.password),
                                         headers=headers, data=json.dumps(payload),
                                         verify=False)

                    if interface in line["untagged"]:
                        vlan_number_id = line[".id"]
                        output_interface_list = []
                        interfaces_in_list = str(line["untagged"]).split(",")
                        for element in interfaces_in_list:
                            if element != interface:
                                output_interface_list.append(element)

                        output_interface_string = ",".join(output_interface_list)
                        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan/{vlan_number_id}"
                        headers = {"content-type": "application/json"}
                        payload = {"untagged": f"{output_interface_string}", ".id": f"{vlan_number_id}"}

                        requests.request(method="PATCH", url=url,
                                         auth=HTTPBasicAuth(self.node.username, self.node.password),
                                         headers=headers, data=json.dumps(payload),
                                         verify=False)
                    break

            if vlan_exist:

                url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan/{number_id}"
                headers = {"content-type": "application/json"}
                payload = {"tagged": f"{tagged}", ".id": f"{number_id}"}

                requests.request(method="PATCH", url=url,
                                 auth=HTTPBasicAuth(self.node.username, self.node.password),
                                 headers=headers, data=json.dumps(payload),
                                 verify=False)

            else:

                url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan/add"
                headers = {"content-type": "application/json"}
                payload = {"bridge": br, "tagged": f"{interface}", "vlan-ids": vlan_id}

                requests.request(method="POST", url=url,
                                 auth=HTTPBasicAuth(self.node.username, self.node.password),
                                 headers=headers, data=json.dumps(payload),
                                 verify=False)

        MikrotikRouterOSSaveConfig(self.node)

    def remove_vlan(self, interface: str, vlan_id: Union[int, str]) -> VlanResume:

        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan"
        headers = {"content-type": "application/json"}

        r = requests.request(method="GET", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers,
                             verify=False)

        for line in r.json():
            if int(line["vlan-ids"]) == int(vlan_id):
                if line["untagged"] == interface:
                    vlan_number_id = line[".id"]
                    url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan/{vlan_number_id}"
                    headers = {"content-type": "application/json"}
                    payload = {"untagged": "", ".id": f"{vlan_number_id}"}

                    requests.request(method="PATCH", url=url,
                                     auth=HTTPBasicAuth(self.node.username, self.node.password),
                                     headers=headers, data=json.dumps(payload),
                                     verify=False)

                if interface in line["untagged"]:
                    vlan_number_id = line[".id"]
                    output_interface_list = []
                    interfaces_in_list = str(line["untagged"]).split(",")
                    for element in interfaces_in_list:
                        if element != interface:
                            output_interface_list.append(element)

                    output_interface_string = ",".join(output_interface_list)
                    url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan/{vlan_number_id}"
                    headers = {"content-type": "application/json"}
                    payload = {"untagged": f"{output_interface_string}", ".id": f"{vlan_number_id}"}

                    requests.request(method="PATCH", url=url,
                                     auth=HTTPBasicAuth(self.node.username, self.node.password),
                                     headers=headers, data=json.dumps(payload),
                                     verify=False)

                if line["tagged"] == interface:
                    vlan_number_id = line[".id"]
                    url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan/{vlan_number_id}"
                    headers = {"content-type": "application/json"}
                    payload = {"tagged": "", ".id": f"{vlan_number_id}"}

                    requests.request(method="PATCH", url=url,
                                     auth=HTTPBasicAuth(self.node.username, self.node.password),
                                     headers=headers, data=json.dumps(payload),
                                     verify=False)

                if interface in line["tagged"]:
                    vlan_number_id = line[".id"]
                    output_interface_list = []
                    interfaces_in_list = str(line["tagged"]).split(",")
                    for element in interfaces_in_list:
                        if element != interface:
                            output_interface_list.append(element)

                    output_interface_string = ",".join(output_interface_list)
                    url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan/{vlan_number_id}"
                    headers = {"content-type": "application/json"}
                    payload = {"tagged": f"{output_interface_string}", ".id": f"{vlan_number_id}"}

                    requests.request(method="PATCH", url=url,
                                     auth=HTTPBasicAuth(self.node.username, self.node.password),
                                     headers=headers, data=json.dumps(payload),
                                     verify=False)

        MikrotikRouterOSSaveConfig(self.node)
        return VlanResume(**{"vlanAccess": self.display_vlan_brief(), "vlanTrunk": self.display_vlan_trunk()})

    def display_vlan_trunk(self) -> list[VlanTrunk]:
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge"
        headers = {"content-type": "application/json"}

        response_bridge = requests.request(method="GET", url=url,
                                           auth=HTTPBasicAuth(self.node.username, self.node.password),
                                           headers=headers,
                                           verify=False)

        protocols: [str] = []
        protocols_dict: dict = {}
        for line in response_bridge.json():
            ether_type = ""
            if line["name"] not in protocols:
                try:
                    if line["ether-type"] == "0x8100":
                        ether_type = "802.1q"
                    elif line["ether-type"] == "0x9100":
                        ether_type = "Double tagged"
                    elif line["ether-type"] == "0x88a8":
                        ether_type = "802.1ad"
                except:
                    ether_type = "802.1q"
                protocols_dict.update({line["name"]: ether_type})

        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/vlan"
        headers = {"content-type": "application/json"}

        response_vlan = requests.request(method="GET", url=url,
                                         auth=HTTPBasicAuth(self.node.username, self.node.password),
                                         headers=headers,
                                         verify=False)

        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/port"
        headers = {"content-type": "application/json"}

        response_port = requests.request(method="GET", url=url,
                                         auth=HTTPBasicAuth(self.node.username, self.node.password),
                                         headers=headers,
                                         verify=False)

        port_trunk_list: list[VlanTrunk] = []
        for port in response_port.json():
            vlan_trunk = []
            for vlan in response_vlan.json():
                if port["interface"] in vlan["tagged"]:
                    vlan_trunk.append(vlan["vlan-ids"])
            mode = ""
            if port["disabled"] == "false":
                mode = "on"
            elif port["disabled"] == "true":
                mode = "off"
            port_trunk = {
                "port": port["interface"],
                "mode": mode,
                "encapsulation": protocols_dict[port["bridge"]],
                "status": "trunking",
                "nativeVlan": port["pvid"],
                "allowedTrunkVlans": vlan_trunk
            }
            port_trunk_list.append(VlanTrunk(**port_trunk))
        return port_trunk_list

    def _check_vlan_bridge_and_create_if_not_exist(self, bridge: str) -> str:

        if bridge is None:
            bridge = "defaultbridge"

        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge"
        headers = {"content-type": "application/json"}
        payload = {"name": bridge}

        r = requests.request(method="GET", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers, data=json.dumps(payload),
                             verify=False)
        line_id = None
        for line in r.json():
            if line["name"] == bridge:
                break

        if line_id is None:
            url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/add"
            headers = {"content-type": "application/json"}
            payload = {"name": bridge}

            requests.request(method="POST", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers, data=json.dumps(payload),
                             verify=False)

            MikrotikRouterOSSaveConfig(self.node)

        return bridge

    def vlan_filtering(self, bridge: str, filtering: str):
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/print"
        headers = {"content-type": "application/json"}

        r = requests.request(method="POST", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers,
                             verify=False)

        bridge_exist: bool = False
        for line in r.json():

            if line["name"] == bridge:
                bridge_exist = True

        if bridge_exist is False:

            url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/add"
            headers = {"content-type": "application/json"}
            payload = {"name": bridge, "vlan-filtering": filtering}

            requests.request(method="POST", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers, data=json.dumps(payload),
                             verify=False)

        else:
            url = f"https://{self.node.ipAddress}:{self.node.port}/rest/interface/bridge/set"
            headers = {"content-type": "application/json"}
            payload = {"name": bridge, "vlan-filtering": filtering, "numbers": bridge}

            requests.request(method="POST", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers, data=json.dumps(payload),
                             verify=False)

        MikrotikRouterOSSaveConfig(self.node)
