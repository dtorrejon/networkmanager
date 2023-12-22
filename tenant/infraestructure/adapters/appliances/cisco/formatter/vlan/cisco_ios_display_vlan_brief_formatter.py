from tenant.domain.schemas.appliances.vlans.vlan_brief import VlanBrief
from tenant.infraestructure.gateways.appliance.formatter.diagnostics.vlan.interface_display_vlan_brief_formatter import \
    IdisplayVlanBriefFormatter


class CiscoIosDisplayVlanBriefFormatter(IdisplayVlanBriefFormatter):

    def format(self, display_text: str) -> list[VlanBrief]:
        input_text_without_headers: str = self._delete_header_lines(display_text, 3)
        text_to_list = input_text_without_headers.split("\n")
        output: list[VlanBrief] = []
        for text_line in text_to_list:
            elements = text_line.split()
            ports = elements[3:]
            output_ports: list[str] = []
            for port in ports:
                output_ports.append(port.rstrip(","))

            vlan_brief: dict = {
                "vlan": int(elements[0]),
                "name": elements[1],
                "status": elements[2],
                "ports": output_ports
            }
            output.append(VlanBrief(**vlan_brief))
        return output

    @staticmethod
    def _delete_header_lines(input_text: str, lines_to_delete: int) -> str:
        lines = input_text.split('\n')
        output_text = '\n'.join(lines[lines_to_delete:])
        return output_text
