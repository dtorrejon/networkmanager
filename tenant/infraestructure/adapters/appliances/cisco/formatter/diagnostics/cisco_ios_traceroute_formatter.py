import ipaddress
import re

from tenant.domain.schemas.appliances.diagnostics.trace_route import TraceRoute
from tenant.domain.schemas.appliances.diagnostics.trace_route_command_fields import TraceRouteCommandFields
from tenant.domain.schemas.appliances.diagnostics.trace_route_hop import TraceRouteHop
from tenant.domain.schemas.appliances.diagnostics.trace_route_probe_count import TraceRouteProbeCount
from tenant.infraestructure.gateways.appliance.formatter.diagnostics.interface_traceroute_formatter import \
    ITraceRouteFormatter


class CiscoIosTraceRouteFormatter(ITraceRouteFormatter):
    def format(self, traceroute_text: str, trace_route_command_fields: TraceRouteCommandFields) -> TraceRoute:
        response_delete_three_first_lines = self._delete_header_lines(traceroute_text)
        response_delete_brackets = self._delete_text_in_brackets(response_delete_three_first_lines)
        response_to_array = self._tracert_text_to_array(response_delete_brackets)
        response_add_ips = self._add_ip_for_each_response(response_to_array)
        add_asterisks = self._replace_asterisks(3, response_add_ips)
        response_replace = add_asterisks.replace("msec", "ms")
        response_dict = self._traceroute_dict(response_replace, trace_route_command_fields.probeCount)

        return TraceRoute(**{"hops": response_dict})

    @staticmethod
    def _delete_header_lines(input_text: str) -> str:
        lines = input_text.split('\n')
        output_text = '\n'.join(lines[4:])
        return output_text

    @staticmethod
    def _delete_text_in_brackets(input_text: str) -> str:
        output_text = re.sub(r'\[.*?]', '', input_text)
        return output_text

    @staticmethod
    def _tracert_text_to_array(input_text: str) -> list[str]:
        input_text = input_text.split("\n")
        output_text = []
        for i, line in enumerate(input_text):
            elements = line.split()
            for element in elements:
                output_text.append(element)
        return output_text

    def _add_ip_for_each_response(self, input_text: list[str]) -> str:
        output_text = input_text
        index = 0
        while index < len(output_text):
            if output_text[index].isdigit() and output_text[index - 1] == "msec" and output_text[index + 1] == "msec":
                reverse_index = index
                while self._is_ipv4(output_text[reverse_index]) is False and reverse_index >= 0:
                    reverse_index -= 1
                output_text.insert(index, output_text[reverse_index])

            if output_text[index].isdigit() and output_text[index - 1] == "*" and output_text[index + 1] == "msec":
                reverse_index = index
                while self._is_ipv4(output_text[reverse_index]) is False and reverse_index >= 0:
                    reverse_index -= 1
                output_text.insert(index, output_text[reverse_index])

            index += 1

        return " ".join(output_text)

    @staticmethod
    def _is_ipv4(ip: str) -> bool:
        try:
            ipaddress.IPv4Address(ip)
            return True
        except ipaddress.AddressValueError:
            return False

    @staticmethod
    def _replace_asterisks(probe_count: int, input_text: str) -> str:
        asterisk: str = "* " * probe_count
        output = input_text.replace("*", asterisk)
        return output

    @staticmethod
    def _traceroute_dict(input_text: str, probe_count_input: int) -> list[TraceRouteHop]:
        probe_count: int = probe_count_input * 3 + 1
        traceroute_answers = []
        temp = []
        input_text = input_text.split()
        for i in range(0, len(input_text)):
            temp.append(input_text[i])
            if ((i + 1) % probe_count) == 0:
                traceroute_answers.append(temp.copy())
                temp.clear()
        hops: list[TraceRouteHop] = []

        for index_traceroute_answer in range(0, len(traceroute_answers)):
            elements = traceroute_answers[index_traceroute_answer]
            hope_number = f"{elements.pop(0)}"
            p_count: list[TraceRouteProbeCount] = []
            hope_id_index = 1
            for index_element in range(0, len(elements), 3):
                hope_id = str(hope_id_index)
                hope_id_index += 1
                ip = elements[index_element]
                time = elements[index_element + 1]
                time_scale = elements[index_element + 2]

                p_count.append(TraceRouteProbeCount(
                    id=f"{hope_id}",
                    ip=f"{ip}",
                    time=f"{time}",
                    timeScale=f"{time_scale}")
                )

            hops.append(TraceRouteHop(hopNumber=hope_number, probeCount=p_count))

        return hops
