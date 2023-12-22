from tenant.domain.schemas.appliances.network_interfaces.network_interface_brief import NetworkInterfaceBrief
from tenant.infraestructure.gateways.appliance.formatter.network_interfaces.interface_display_brief_formatter import \
    IdisplayBriefFormatter


class CiscoIosDisplayInterfaceBriefFormatter(IdisplayBriefFormatter):
    def format(self, display_brief_text: str) -> list[NetworkInterfaceBrief]:
        input_text_without_headers: str = self._delete_header_lines(display_brief_text, 1)
        text_to_list = input_text_without_headers.split("\n")
        output: list[NetworkInterfaceBrief] = []
        for text_line in text_to_list:
            elements = text_line.split()

            output_dict: dict = {
                "name": "",
                "ipAddress": "",
                "status": "",
                "protocol": ""
            }
            output_dict.update({"name": elements[0], "ipAddress": elements[1], "protocol": elements[-1]})

            if elements[4].lower() == "administratively":
                output_dict.update({"status": f"{elements[4]} {elements[5]}"})
            else:
                output_dict.update({"status": f"{elements[4]}"})
            output.append(NetworkInterfaceBrief(**output_dict))
        return output

    @staticmethod
    def _delete_header_lines(input_text: str, lines_to_delete: int) -> str:
        lines = input_text.split('\n')
        output_text = '\n'.join(lines[lines_to_delete:])
        return output_text
