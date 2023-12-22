from unittest.mock import Mock
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.application.usecases.appliance.network_interfaces.display_network_interfaces import DisplayNetworkInterfaces
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class TestDisplayNetworkInterfaces:
    @staticmethod
    def test_return_network_interface_list_when_display_is_called_with_valid_interface():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.display.return_value = [NetworkInterface(**{"name": "Ethernet0/0", "description": "",
                                                                   "macAddress": "aabb.cc00.0100",
                                                                   "ipAddress": "unassigned", "mtu": 1500,
                                                                   "status": "up",
                                                                   "protocol": "up"})]

        usecase = DisplayNetworkInterfaces(mock_appliance)
        result = usecase.display("valid_interface")

        assert len(result) > 0
        assert isinstance(result[0], NetworkInterface)

    @staticmethod
    def test_raise_exception_when_display_is_called_with_invalid_interface():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.display.side_effect = Exception

        usecase = DisplayNetworkInterfaces(mock_appliance)

        try:
            usecase.display("invalid_interface")
            assert False
        except Exception:
            assert True
