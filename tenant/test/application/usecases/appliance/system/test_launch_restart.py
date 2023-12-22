from unittest.mock import Mock
from tenant.application.usecases.appliance.system.launch_restart import LaunchRestart
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance
from tenant.domain.schemas.appliances.system.restart import Restart


class TestLaunchRestart:

    @staticmethod
    def test_return_restart_when_restart_is_called():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.restart.return_value = Restart(**{
            "status": "KO",
            "message": "Can't reboot device. Configuration register is 0x0, and must be 0x2102"
        })

        usecase = LaunchRestart(mock_appliance)
        result = usecase.restart()

        assert isinstance(result, Restart)

    @staticmethod
    def test_raise_exception_when_restart_is_called_and_appliance_raises_exception():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.restart.side_effect = Exception

        usecase = LaunchRestart(mock_appliance)

        try:
            usecase.restart()
            assert False
        except Exception:
            assert True
