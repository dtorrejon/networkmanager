from unittest.mock import Mock
from tenant.domain.schemas.appliances.commands.command import Command
from tenant.application.usecases.appliance.commands.send_command import SendCommand
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class TestSendCommand:
    @staticmethod
    def test_return_command_when_send_command_is_called_with_valid_command():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.send_command.return_value = Command(**{"command": "show vlan brief",
                "response": f"response"})

        usecase = SendCommand(mock_appliance)
        result = usecase.send_command("valid_command")

        assert isinstance(result, Command)
    @staticmethod
    def test_raise_exception_when_send_command_is_called_with_invalid_command():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.send_command.side_effect = Exception

        usecase = SendCommand(mock_appliance)

        try:
            usecase.send_command("invalid_command")
            assert False
        except Exception:
            assert True
    @staticmethod
    def test_return_none_when_send_command_is_called_with_no_command():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.send_command.return_value = None

        usecase = SendCommand(mock_appliance)
        result = usecase.send_command(None)

        assert result is None
