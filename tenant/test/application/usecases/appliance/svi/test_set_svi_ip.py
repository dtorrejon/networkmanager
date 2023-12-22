from unittest.mock import Mock
from tenant.application.usecases.appliance.svi.set_svi_ip import SetSviIp
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface


class TestSetSviIp:
    @staticmethod
    def test_return_network_interface_when_set_svi_ip_is_called_with_valid_svi_and_ip_address():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_svi_ip.return_value = NetworkInterface(**{"name": "vlan60", "description": "",
                                                                     "macAddress": "aabb.cc00.0100",
                                                                     "ipAddress": "unassigned", "mtu": 1500,
                                                                     "status": "up",
                                                                     "protocol": "up"})

        usecase = SetSviIp(mock_appliance)
        result = usecase.set_svi_ip("valid_svi", "valid_ip_address")

        assert isinstance(result, NetworkInterface)

    @staticmethod
    def test_raise_exception_when_set_svi_ip_is_called_with_invalid_svi():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_svi_ip.side_effect = Exception

        usecase = SetSviIp(mock_appliance)

        try:
            usecase.set_svi_ip("invalid_svi", "valid_ip_address")
            assert False
        except Exception:
            assert True

    @staticmethod
    def test_return_none_when_set_svi_ip_is_called_with_no_svi():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_svi_ip.return_value = None

        usecase = SetSviIp(mock_appliance)
        result = usecase.set_svi_ip(None, "valid_ip_address")

        assert result is None

    @staticmethod
    def test_return_none_when_set_svi_ip_is_called_with_no_ip_address():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_svi_ip.return_value = None

        usecase = SetSviIp(mock_appliance)
        result = usecase.set_svi_ip("valid_svi", None)

        assert result is None
