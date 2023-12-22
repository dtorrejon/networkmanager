from tenant.domain.schemas.appliances.diagnostics.arp import Arp
from tenant.infraestructure.gateways.appliance.formatter.diagnostics.interface_arp_formatter import \
    IArpFormatter


class CiscoIosArpFormatter(IArpFormatter):
    def format(self, arp_text: str) -> list[Arp]:
        lines = arp_text.split('\n')
        lines = [line.strip() for line in lines if line.strip()]

        keys: list[str] = ["protocol", "ipAddress", "age", "macAddress", "type", "interface"]

        response: list[Arp] = []
        for line in lines[1:]:
            values = line.split()
            line_dict = {}
            for i in range(len(keys)):
                line_dict[keys[i]] = values[i]
            response.append(Arp(**line_dict))

        return response
