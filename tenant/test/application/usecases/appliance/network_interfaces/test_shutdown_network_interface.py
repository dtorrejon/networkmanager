from unittest.mock import Mock
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.application.usecases.appliance.network_interfaces.shutdown_network_interface import ShutdownNetworkInterface
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class TestShutdownNetworkInterface:
    @staticmethod
    def test_return_network_interface_when_shutdown_is_called_with_valid_interface():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.shutdown.return_value = NetworkInterface(**{"name": "Ethernet0/0", "description": "",
                                                                   "macAddress": "aabb.cc00.0100",
                                                                   "ipAddress": "unassigned", "mtu": 1500,
                                                                   "status": "up",
                                                                   "protocol": "up"})

        usecase = ShutdownNetworkInterface(mock_appliance)
        result = usecase.shutdown("valid_interface")

        assert isinstance(result, NetworkInterface)

    @staticmethod
    def test_raise_exception_when_shutdown_is_called_with_invalid_interface():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.shutdown.side_effect = Exception

        usecase = ShutdownNetworkInterface(mock_appliance)

        try:
            usecase.shutdown("invalid_interface")
            assert False
        except Exception:
            assert True

    @staticmethod
    def test_return_none_when_shutdown_is_called_with_no_interface():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.shutdown.return_value = None

        usecase = ShutdownNetworkInterface(mock_appliance)
        result = usecase.shutdown(None)

        assert result is None
