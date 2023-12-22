from unittest.mock import Mock
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.application.usecases.appliance.network_interfaces.no_shutdown_network_interface import \
    NoShutdownNetworkInterface
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class TestNoShutdownNetworkInterface:
    @staticmethod
    def test_return_network_interface_when_no_shutdown_is_called_with_valid_interface():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.no_shutdown.return_value = NetworkInterface(**{"name": "Ethernet0/0", "description": "",
                                                                      "macAddress": "aabb.cc00.0100",
                                                                      "ipAddress": "unassigned", "mtu": 1500,
                                                                      "status": "up",
                                                                      "protocol": "up"})

        usecase = NoShutdownNetworkInterface(mock_appliance)
        result = usecase.no_shutdown("valid_interface")

        assert isinstance(result, NetworkInterface)

    @staticmethod
    def test_raise_exception_when_no_shutdown_is_called_with_invalid_interface():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.no_shutdown.side_effect = Exception

        usecase = NoShutdownNetworkInterface(mock_appliance)

        try:
            usecase.no_shutdown("invalid_interface")
            assert False
        except Exception:
            assert True

    @staticmethod
    def test_return_none_when_no_shutdown_is_called_with_no_interface():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.no_shutdown.return_value = None

        usecase = NoShutdownNetworkInterface(mock_appliance)
        result = usecase.no_shutdown(None)

        assert result is None
