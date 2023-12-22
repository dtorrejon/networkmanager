import json
import urllib3
import requests
from requests.auth import HTTPBasicAuth

from tenant.domain.schemas.appliances.diagnostics.arp import Arp
from tenant.domain.schemas.appliances.diagnostics.ping import Ping
from tenant.domain.schemas.appliances.diagnostics.ping_command_fields import PingCommandFields
from tenant.domain.schemas.appliances.diagnostics.trace_route import TraceRoute
from tenant.domain.schemas.appliances.diagnostics.trace_route_command_fields import TraceRouteCommandFields
from tenant.domain.schemas.appliances.diagnostics.trace_route_hop import TraceRouteHop
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.infraestructure.gateways.appliance.interface_diagnostics import IDiagnostics


class MikrotikRouterOSDiagnostics(IDiagnostics):

    def __init__(self, node: NodeWithCredentials):
        self.node = node
        urllib3.disable_warnings()

    def obtain_interface_from_ip(self, ip: str):

        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/ip/address"
        response = requests.request(method="GET", url=url, auth=HTTPBasicAuth(self.node.username, self.node.password),
                                    verify=False)

        for address in response.json():
            if ip in address['address']:
                return address['interface']

        return None

    def ping(self, ping_command_fields: PingCommandFields) -> Ping:

        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/ping"
        headers = {"content-type": "application/json"}

        if ping_command_fields.sourceIpAddress is None:
            payload = {"address": ping_command_fields.destinationIpAddress, "count": ping_command_fields.repeat}
        else:
            payload = {"interface": self.obtain_interface_from_ip(ping_command_fields.sourceIpAddress),
                       "address": ping_command_fields.destinationIpAddress,
                       "count": ping_command_fields.repeat}

        ping_response = requests.request(method="POST", url=url,
                                         auth=HTTPBasicAuth(self.node.username, self.node.password),
                                         headers=headers, data=json.dumps(payload),
                                         verify=False)

        percent = int(ping_response.json()[-1]['sent']) / int(ping_response.json()[-1]['received']) * 100

        if ping_command_fields.sourceIpAddress is None:
            source = "Not Defined"
        else:
            source = ping_command_fields.sourceIpAddress

        return Ping(**{
            "source": source,
            "destination": ping_response.json()[-1]['host'],
            "packetsTransmitted": ping_response.json()[-1]['sent'],
            "packetsReceived": ping_response.json()[-1]['received'],
            "percent": f"{percent}%",
            "roundTrip": {
                "min": ping_response.json()[-1]['min-rtt'],
                "avg": ping_response.json()[-1]['avg-rtt'],
                "max": ping_response.json()[-1]['max-rtt']
            }
        })

    def traceroute(self, trace_route_command_fields: TraceRouteCommandFields) -> TraceRoute:
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/tool/traceroute"
        headers = {"content-type": "application/json"}
        payload = {"address": trace_route_command_fields.destinationIpAddress,
                   "count": trace_route_command_fields.probeCount}

        traceroute_response = requests.request(method="POST", url=url,
                                               auth=HTTPBasicAuth(self.node.username, self.node.password),
                                               headers=headers, data=json.dumps(payload),
                                               verify=False)

        result = {}
        for item in traceroute_response.json():
            section_value = item.get(".section")
            if section_value is not None:
                if section_value not in result:
                    result[section_value] = []
                result[section_value].append(item)

        sorted_sublists = sorted(result.values(), key=len, reverse=True)
        top_sublists = sorted_sublists[:int(trace_route_command_fields.probeCount)]

        output = []

        id = 1
        for list in top_sublists:
            for element in list:
                if element["address"] != '' and element["address"] != trace_route_command_fields.destinationIpAddress:
                    output.append(
                        {"id": str(id), "ip": element["address"], "time": element["last"], "timeScale": "ms"})

                elif element["address"] == '':
                    output.append({"id": str(id), "ip": "*", "time": "*", "timeScale": "ms"})

                elif element["address"] == trace_route_command_fields.destinationIpAddress:
                    output.append(
                        {"id": str(id), "ip": element["address"], "time": element["last"], "timeScale": "ms"})
                    id += 1

        hops = len(output)
        elements_list = []
        hop = 0
        while hop < hops / trace_route_command_fields.probeCount:
            line = {"hopNumber": str(hop + 1),
                    "probeCount": output[hop::int(hops / trace_route_command_fields.probeCount)]}
            elements_list.append(line)
            hop += 1

        output_list = []

        for element in elements_list:
            output_list.append(element)

        j = json.dumps({"hops": output_list}, indent=4)
        tr: dict = json.loads(j)
        return TraceRoute(**tr)

    def arp(self) -> list[Arp]:
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/ip/arp"
        headers = {"content-type": "application/json"}

        arp_response = requests.request(method="GET", url=url,
                                        auth=HTTPBasicAuth(self.node.username, self.node.password),
                                        headers=headers,
                                        verify=False)

        output = []
        for line in arp_response.json():
            arp_line = {
                "protocol": "Internet",
                "ipAddress": line["address"],
                "macAddress": line["mac-address"],
                "age": "-",
                "type": "-",
                "interface": line["interface"]
            }
            output.append(Arp(**arp_line))

        return output
