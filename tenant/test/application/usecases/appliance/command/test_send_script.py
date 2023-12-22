from unittest.mock import Mock
from tenant.domain.schemas.appliances.commands.command import Command
from tenant.domain.schemas.appliances.commands.script import Script
from tenant.application.usecases.appliance.commands.send_script import SendScript
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class TestSendScript:
    @staticmethod
    def test_return_commands_when_send_script_is_called_with_valid_script():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.send_script.return_value = [Command(**{"command": "show vlan brief",
                                                              "response": f"response"}),
                                                   Command(**{"command": "show vlan brief 2",
                                                              "response": f"response2"})]
        s = Script(**{"commands": ["cmd1", "cmd2"]})

        usecase = SendScript(mock_appliance)
        result = usecase.send_script(s)

        assert len(result) > 0
        assert isinstance(result[0], Command)

    @staticmethod
    def test_raise_exception_when_send_script_is_called_with_invalid_script():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.send_script.side_effect = Exception

        usecase = SendScript(mock_appliance)

        try:
            usecase.send_script("invalid_script")
            assert False
        except Exception:
            assert True

    @staticmethod
    def test_return_empty_list_when_send_script_is_called_with_no_script():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.send_script.return_value = []

        usecase = SendScript(mock_appliance)
        result = usecase.send_script(None)

        assert len(result) == 0
