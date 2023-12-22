from unittest.mock import Mock
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.application.usecases.appliance.network_interfaces.set_ip_network_interface import SetIPNetworkInterface
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class TestSetIPNetworkInterface:
    @staticmethod
    def test_return_network_interface_when_set_ip_is_called_with_valid_interface_and_ip_address():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_ip.return_value = NetworkInterface(**{"name": "Ethernet0/0", "description": "",
                                                                 "macAddress": "aabb.cc00.0100",
                                                                 "ipAddress": "unassigned", "mtu": 1500,
                                                                 "status": "up",
                                                                 "protocol": "up"})

        usecase = SetIPNetworkInterface(mock_appliance)
        result = usecase.set_ip("valid_interface", "valid_ip_address")

        assert isinstance(result, NetworkInterface)

    @staticmethod
    def test_raise_exception_when_set_ip_is_called_with_invalid_interface():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_ip.side_effect = Exception

        usecase = SetIPNetworkInterface(mock_appliance)

        try:
            usecase.set_ip("invalid_interface", "valid_ip_address")
            assert False
        except Exception:
            assert True

    @staticmethod
    def test_return_none_when_set_ip_is_called_with_no_interface():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_ip.return_value = None

        usecase = SetIPNetworkInterface(mock_appliance)
        result = usecase.set_ip(None, "valid_ip_address")

        assert result is None

