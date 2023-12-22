import pytest
from tenant.infraestructure.adapters.appliances.cisco.formatter.system.cisco_ios_restart_fomatter import \
    CiscoIosRestartFormatter
from tenant.domain.schemas.appliances.system.restart import Restart


class TestCiscoIosRestartFormatter:
    def test_format_restart_text_with_unexpected_response(self):
        formatter = CiscoIosRestartFormatter()
        restart_text = "Unexpected response"
        result = formatter.format(restart_text)
        assert isinstance(result, Restart)
        assert result.status == "nok"
        assert result.message == "Can't reboot device."


