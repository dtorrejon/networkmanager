import ipaddress
import re

from tenant.domain.models.cisco_route_codes import CiscoRouteCodes
from tenant.domain.schemas.appliances.diagnostics.route import Route
from tenant.infraestructure.gateways.appliance.formatter.routing.interface_routing_table_formatter import \
    IRoutingTableFormatter


class CiscoIosRoutingTableFormatter(IRoutingTableFormatter):

    def format(self, routing_table_text: str) -> list[Route]:


        routes_with_initial_text = routing_table_text.split("\n")
        first_route_line_detected: bool = False
        route_lines = []

        for text_line in routes_with_initial_text:
            elements = text_line.split()
            if elements != []:
                if (first_route_line_detected and not self._is_ipv4(elements[0]) and elements[0] in
                        CiscoRouteCodes.get_values_in_a_string()):
                    route_lines.append(elements)

                if elements[0] == "Gateway" and elements[1] == "of" and elements[2] == "last":
                    first_route_line_detected = True
        for index, route_line in enumerate(route_lines):
            if route_line[0] != CiscoRouteCodes.OSPF.value and route_line[0] != CiscoRouteCodes.IS_IS.value:
                route_lines[index].insert(1, "-")

        routes_output: list[Route] = []
        route_index: int = 0

        for index, route_line in enumerate(route_lines):
            if route_line[1] == "-":
                protocol = CiscoRouteCodes(route_line[0]).name
            else:
                protocol = f"{CiscoRouteCodes(route_line[0]).name} {CiscoRouteCodes(route_line[1]).name}"
                protocol.replace("_", " ")

            destination_network = route_line[2]
            pattern = r"\[(\d+)\/(\d+)\]"

            if route_line[3] == "is" and route_line[4] == "directly":
                route_index += 1
                route = Route(**{
                    "id": route_index,
                    "destination": destination_network,
                    "protocol": protocol,
                    "preference": 0,
                    "cost": 0,
                    "nextHop": f"{route_line[4]}",
                    "interface": f"{route_line[-1]}",
                    "age": "-"})

                routes_output.append(route)

            elif re.match(pattern, route_line[3]):
                route_index += 1
                matches = re.findall(pattern, route_line[3])
                age: str
                try:
                    age = route_line[6]
                except IndexError:
                    age = "-"

                route = Route(**{
                    "id": route_index,
                    "destination": destination_network,
                    "protocol": protocol,
                    "preference": f"{matches[0][0]}",
                    "cost": f"{matches[0][1]}",
                    "nextHop": f"{route_line[5]}",
                    "interface": f"{route_line[-1]}",
                    "age": f"{age}"
                })
                routes_output.append(route)
        return routes_output

    @staticmethod
    def _is_ipv4(ip: str) -> bool:
        try:
            ipaddress.IPv4Network(ip)
            return True
        except ipaddress.AddressValueError:
            return False
