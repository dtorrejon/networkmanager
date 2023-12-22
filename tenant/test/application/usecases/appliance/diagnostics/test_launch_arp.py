from unittest.mock import Mock
from tenant.domain.schemas.appliances.diagnostics.arp import Arp
from tenant.application.usecases.appliance.diagnostics.launch_arp import LaunchArp
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance
class TestLaunchArp:
    @staticmethod
    def test_return_arp_list_when_arp_is_called():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.arp.return_value = [Arp()]

        usecase = LaunchArp(mock_appliance)
        result = usecase.arp()

        assert len(result) > 0
        assert isinstance(result[0], Arp)
    @staticmethod
    def test_raise_exception_when_arp_is_called_and_appliance_raises_exception():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.arp.side_effect = Exception

        usecase = LaunchArp(mock_appliance)

        try:
            usecase.arp()
            assert False
        except Exception:
            assert True
    @staticmethod
    def test_return_empty_list_when_arp_is_called_and_appliance_returns_empty_list():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.arp.return_value = []

        usecase = LaunchArp(mock_appliance)
        result = usecase.arp()

        assert len(result) == 0
