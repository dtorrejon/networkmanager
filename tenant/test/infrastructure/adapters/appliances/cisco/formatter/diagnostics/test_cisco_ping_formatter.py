from tenant.domain.schemas.appliances.diagnostics.ping import Ping
from tenant.infraestructure.adapters.appliances.cisco.formatter.diagnostics.cisco_ios_ping_formatter import \
    CiscoIosPingFormatter


class TestCiscoIosPingFormatter:
    @staticmethod
    def test_format_ping_text():
        ping_formatter = CiscoIosPingFormatter()
        ping_text = "Type escape sequence to abort.\n" \
                    "Sending 5, 100-byte ICMP Echos to 192.168.1.1, timeout is 2 seconds:\n" \
                    "!!!!!\n" \
                    "Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/1 ms"
        result = ping_formatter.format("192.169.20.10", "192.168.1.1", ping_text)
        assert isinstance(result, Ping)
        assert result.source == "192.169.20.10"
        assert result.destination == "192.168.1.1"
        assert result.packetsTransmitted == 5
        assert result.packetsReceived == 5
        assert result.percent == "100%"
        assert result.roundTrip.min == "1 ms"
        assert result.roundTrip.avg == "1 ms"
        assert result.roundTrip.max == "1 ms"

    @staticmethod
    def test_format_ping_text_lost_packets():
        ping_formatter = CiscoIosPingFormatter()
        ping_text = "Type escape sequence to abort.\n" \
                    "Sending 5, 100-byte ICMP Echos to 192.168.1.1, timeout is 2 seconds:\n" \
                    ".!!!\n" \
                    "Success rate is 80 percent (4/5), round-trip min/avg/max = 1/1/1 ms"
        result = ping_formatter.format("192.169.20.10", "192.168.1.1", ping_text)
        assert isinstance(result, Ping)
        assert result.source == "192.169.20.10"
        assert result.destination == "192.168.1.1"
        assert result.packetsTransmitted == 5
        assert result.packetsReceived == 4
        assert result.percent == "80%"
        assert result.roundTrip.min == "1 ms"
        assert result.roundTrip.avg == "1 ms"
        assert result.roundTrip.max == "1 ms"
