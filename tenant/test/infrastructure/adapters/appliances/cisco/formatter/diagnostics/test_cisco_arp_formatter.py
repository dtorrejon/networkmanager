import pytest
from tenant.infraestructure.adapters.appliances.cisco.formatter.diagnostics.cisco_ios_arp_formatter import \
    CiscoIosArpFormatter
from tenant.domain.schemas.appliances.diagnostics.arp import Arp


class TestCiscoIosArpFormatter:
    @staticmethod
    def test_format_arp_text():
        arp_formatter = CiscoIosArpFormatter()
        arp_text = "Protocol  Address          Age (min)  Hardware Addr   Type   Interface\n" \
                   "Internet  192.168.1.1             -   0011.2233.4455  ARPA   GigabitEthernet0/0\n" \
                   "Internet  192.168.1.2             5   5566.7788.9900  ARPA   GigabitEthernet0/0"
        result = arp_formatter.format(arp_text)
        assert len(result) == 2
        assert isinstance(result[0], Arp)
        assert result[0].protocol == "Internet"
        assert result[0].ipAddress == "192.168.1.1"
        assert result[0].age == "-"
        assert result[0].macAddress == "0011.2233.4455"
        assert result[0].type == "ARPA"
        assert result[0].interface == "GigabitEthernet0/0"
        assert isinstance(result[1], Arp)
        assert result[1].protocol == "Internet"
        assert result[1].ipAddress == "192.168.1.2"
        assert result[1].age == "5"
        assert result[1].macAddress == "5566.7788.9900"
        assert result[1].type == "ARPA"
        assert result[1].interface == "GigabitEthernet0/0"
    @staticmethod
    def test_format_arp_text_empty():
        arp_formatter = CiscoIosArpFormatter()
        arp_text = ""
        result = arp_formatter.format(arp_text)
        assert len(result) == 0
    @staticmethod
    def test_format_arp_text_no_lines():
        arp_formatter = CiscoIosArpFormatter()
        arp_text = "Protocol  Address          Age (min)  Hardware Addr   Type   Interface"
        result = arp_formatter.format(arp_text)
        assert len(result) == 0
