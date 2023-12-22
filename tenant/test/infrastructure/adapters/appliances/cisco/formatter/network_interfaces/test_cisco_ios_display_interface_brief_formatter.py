import pytest
from tenant.infraestructure.adapters.appliances.cisco.formatter.network_interfaces.cisco_ios_display_interface_brief_formatter import \
    CiscoIosDisplayInterfaceBriefFormatter
from tenant.domain.schemas.appliances.network_interfaces.network_interface_brief import NetworkInterfaceBrief


class TestCiscoIosDisplayInterfaceBriefFormatter:
    @staticmethod
    def test_format_valid_display_brief_text():
        formatter = CiscoIosDisplayInterfaceBriefFormatter()
        display_brief_text = "Interface              IP-Address      OK? Method Status                Protocol\n" \
                             "GigabitEthernet0/0     192.168.1.1     YES NVRAM  up                    up"
        result = formatter.format(display_brief_text)
        assert len(result) == 1
        assert isinstance(result[0], NetworkInterfaceBrief)
        assert result[0].name == "GigabitEthernet0/0"
        assert result[0].ipAddress == "192.168.1.1"
        assert result[0].status == "up"
        assert result[0].protocol == "up"

    @staticmethod
    def test_format_display_brief_text_multiple_interfaces():
        formatter = CiscoIosDisplayInterfaceBriefFormatter()
        display_brief_text = "Interface              IP-Address      OK? Method Status                Protocol\n" \
                             "GigabitEthernet0/0     192.168.1.1     YES NVRAM  up                    up\n" \
                             "GigabitEthernet0/1     192.168.1.2     YES NVRAM  administratively down down"
        result = formatter.format(display_brief_text)
        assert len(result) == 2
        assert isinstance(result[0], NetworkInterfaceBrief)
        assert result[0].name == "GigabitEthernet0/0"
        assert result[0].ipAddress == "192.168.1.1"
        assert result[0].status == "up"
        assert result[0].protocol == "up"
        assert isinstance(result[1], NetworkInterfaceBrief)
        assert result[1].name == "GigabitEthernet0/1"
        assert result[1].ipAddress == "192.168.1.2"
        assert result[1].status == "administratively down"
        assert result[1].protocol == "down"
