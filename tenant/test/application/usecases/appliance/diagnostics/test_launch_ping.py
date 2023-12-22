from unittest.mock import Mock
from tenant.domain.schemas.appliances.diagnostics.ping import Ping
from tenant.domain.schemas.appliances.diagnostics.ping_command_fields import PingCommandFields
from tenant.application.usecases.appliance.diagnostics.launch_ping import LaunchPing
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class TestLaunchPing:
    @staticmethod
    def test_return_ping_when_ping_is_called_with_valid_command_fields():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.ping.return_value = Ping(**{
                "source": "192.168.20.10",
                "destination": "8.8.8.8",
                "packetsTransmitted": 4,
                "packetsReceived": 4,
                "percent": "100%",
                "roundTrip": {
                    "min": "26 ms",
                    "avg": "38 ms",
                    "max": "51 ms"
                }})

        usecase = LaunchPing(mock_appliance)
        result = usecase.ping(PingCommandFields(**{"sourceIpAddress": "1.1.1.1", "destinationIpAddress": "8.8.8.8", "repeat": 4}))

        assert isinstance(result, Ping)

    @staticmethod
    def test_raise_exception_when_ping_is_called_with_invalid_command_fields():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.ping.side_effect = Exception

        usecase = LaunchPing(mock_appliance)

        try:
            usecase.ping("invalid_command_fields")
            assert False
        except Exception:
            assert True

    @staticmethod
    def test_return_none_when_ping_is_called_with_no_command_fields():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.ping.return_value = None

        usecase = LaunchPing(mock_appliance)
        result = usecase.ping(None)

        assert result is None
