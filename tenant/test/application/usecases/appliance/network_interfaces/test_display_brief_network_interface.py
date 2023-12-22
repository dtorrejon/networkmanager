from unittest.mock import Mock
from tenant.domain.schemas.appliances.network_interfaces.network_interface_brief import NetworkInterfaceBrief
from tenant.application.usecases.appliance.network_interfaces.display_brief_network_interface import \
    DisplayBriefNetworkInterface
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance

class TestDisplayBriefNetworkInterface:
    @staticmethod
    def test_return_network_interface_brief_list_when_display_brief_is_called():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.display_interface_brief.return_value = [NetworkInterfaceBrief(**{"name": "Ethernet0/0", "ipAddress":
            "unassigned", "status": "up", "protocol": "up"}), NetworkInterfaceBrief(**{"name": "Ethernet0/1", "ipAddress":
            "unassigned", "status": "up", "protocol": "up" })]

        usecase = DisplayBriefNetworkInterface(mock_appliance)
        result = usecase.display_brief()

        assert len(result) > 0
        assert isinstance(result[0], NetworkInterfaceBrief)

    @staticmethod
    def test_raise_exception_when_display_brief_is_called_and_appliance_raises_exception():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.display_interface_brief.side_effect = Exception

        usecase = DisplayBriefNetworkInterface(mock_appliance)

        try:
            usecase.display_brief()
            assert False
        except Exception:
            assert True

    @staticmethod
    def test_return_empty_list_when_display_brief_is_called_and_appliance_returns_empty_list():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.display_interface_brief.return_value = []

        usecase = DisplayBriefNetworkInterface(mock_appliance)
        result = usecase.display_brief()

        assert len(result) == 0
