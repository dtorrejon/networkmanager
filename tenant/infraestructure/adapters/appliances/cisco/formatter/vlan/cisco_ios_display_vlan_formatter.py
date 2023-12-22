from tenant.domain.schemas.appliances.vlans.vlan_trunk import VlanTrunk
from tenant.infraestructure.gateways.appliance.formatter.diagnostics.vlan.interface_display_vlan_formatter import \
    IdisplayVlanFormatter


class CiscoDisplayVlanTrunkFormatter(IdisplayVlanFormatter):

    def format(self, display_text: str) -> list[VlanTrunk]:
        lines_number: int = len(display_text.split('\n'))

        section_one_text = "\n".join(display_text.split('\n')[0:int(lines_number / 4 - 1)])

        section_two_text = "\n".join(display_text.split('\n')[int(lines_number / 4):int(lines_number / 2 - 1)])

        section_one_text_without_header = self._delete_header_lines(section_one_text, 2)
        section_two_text_without_header = self._delete_header_lines(section_two_text, 2)

        output: list[VlanTrunk] = []

        for index, elements in enumerate(section_one_text_without_header.split("\n")):
            vlans: list[int] = []
            allowed_trunk_vlans = section_two_text_without_header.split("\n")[index].split()[-1]
            if "-" in allowed_trunk_vlans:
                down_limit = int(allowed_trunk_vlans.split("-")[0])
                up_limit = int(allowed_trunk_vlans.split("-")[1])
                vlans = list(range(down_limit, up_limit+1))
            elif allowed_trunk_vlans == 'none':
                vlans = []
            else:
                for vlan in allowed_trunk_vlans.split(","):
                    vlans.append(int(vlan))
            output_elements = elements.split()
            output_dict = {
                "port": output_elements[0],
                "mode": output_elements[1],
                "encapsulation": output_elements[2],
                "status": output_elements[3],
                "nativeVlan": output_elements[4],
                "allowedTrunkVlans": vlans
            }
            vlan_trunk = VlanTrunk(**output_dict)
            output.append(vlan_trunk)
        return output


    @staticmethod
    def _delete_header_lines(input_text: str, lines_to_delete: int) -> str:
        lines = input_text.split('\n')
        output_text = '\n'.join(lines[lines_to_delete:])
        return output_text
