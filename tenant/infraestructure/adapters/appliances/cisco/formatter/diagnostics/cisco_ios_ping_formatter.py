import json
import re

from tenant.domain.schemas.appliances.diagnostics.ping import Ping
from tenant.infraestructure.gateways.appliance.formatter.diagnostics.interface_ping_formatter import \
    IPingFormatter


class CiscoIosPingFormatter(IPingFormatter):
    def format(self, source: str, destination: str, response: str) -> Ping:

        transmitted_match = re.search(r'Sending (\d+),', response)
        received_match = re.search(r'Success rate is (\d+) percent \((\d+)/(\d+)\),', response)
        round_trip_match = re.search(r'round-trip min/avg/max = (\d+)/(\d+)/(\d+)', response)

        packets_transmitted: int = 0
        result: json = {}

        if transmitted_match:
            packets_transmitted = int(transmitted_match.group(1))

        if received_match and round_trip_match:
            packets_received = int(received_match.group(2))
            round_trip_min = round_trip_match.group(1) + ' ms'
            round_trip_avg = round_trip_match.group(2) + ' ms'
            round_trip_max = round_trip_match.group(3) + ' ms'
            percent = '{:.0%}'.format(packets_received / packets_transmitted)

            result: dict = {
                "source": source,
                "destination": destination,
                "packetsTransmitted": packets_transmitted,
                "packetsReceived": packets_received,
                "percent": percent,
                "roundTrip": {
                    "min": round_trip_min,
                    "avg": round_trip_avg,
                    "max": round_trip_max
                }
            }

        if f"Success rate is 0 percent (0/5)" in response:
            result: dict = {
                "packetsTransmitted": packets_transmitted,
                "packetsReceived": 0,
                "percent": f"0%",
                "roundTrip": {
                    "min": "",
                    "avg": "",
                    "max": ""
                }
            }

        return Ping(**result)