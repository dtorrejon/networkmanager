from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.infraestructure.gateways.appliance.formatter.network_interfaces.interface_display_formatter import \
    IdisplayInterfaceFormatter


class CiscoIosDisplayInterfaceInterfaceFormatter(IdisplayInterfaceFormatter):
    def format(self, display_text: str) -> list[NetworkInterface]:
        text_to_list = display_text.split("\n")
        interfaces: list[str] = self.get_interfaces(text_to_list)

        if len(interfaces) == 0:
            return []

        output_interface_lines = []

        network_interface: dict = {
            "name": "",
            "macAddress": "",
            "ipAddress": "unassigned",
            "description": "",
            "mtu": 0,
            "status": "",
            "protocol": ""
        }

        for text_line in text_to_list:
            elements = text_line.split()

            for element in elements:
                if element in interfaces:
                    network_interface.update({"name": element})
                    if elements[elements.index(element) + 2] == "administratively":
                        network_interface.update({
                            "status": f"{elements[elements.index(element) + 2]} {elements[elements.index(element) + 3].strip(',')}"})
                    else:
                        network_interface.update({"status": f"{elements[elements.index(element) + 2].strip(',')}"})

                    if "Vlan" in network_interface.get("name"):
                        network_interface.update({"protocol": elements[-1]})
                    else:
                        network_interface.update({"protocol": elements[-2]})

                elif element == "Hardware":
                    network_interface.update({"macAddress": elements[-3]})
                elif element == "Description:":
                    network_interface.update({"description": " ".join(elements[1:])})
                elif element == "Internet":
                    network_interface.update({"ipAddress": elements[-1]})
                elif element == "MTU":
                    network_interface.update({"mtu": int(elements[elements.index(element) + 1])})

            if network_interface.get("name") != "" and network_interface.get(
                    "macAddress") != "" and network_interface.get("status") != "" and network_interface.get(
                "protocol") != "" and network_interface.get("mtu") != 0:
                output_interface_lines.append(network_interface)
                network_interface = {
                    "name": "",
                    "macAddress": "",
                    "ipAddress": "unassigned",
                    "description": "",
                    "mtu": 0,
                    "status": "",
                    "protocol": ""
                }

        output_response: list[NetworkInterface] = []

        for output_network_interface in output_interface_lines:
            output_response.append(NetworkInterface(**output_network_interface))

        return output_response

    @staticmethod
    def get_interfaces(text_list: list[str]) -> list:
        interfaces: list = []
        try:
            for text_line in text_list:
                if text_line[0] != " ":
                    interfaces.append(text_line.split()[0])

            return interfaces

        except IndexError:
            return []
