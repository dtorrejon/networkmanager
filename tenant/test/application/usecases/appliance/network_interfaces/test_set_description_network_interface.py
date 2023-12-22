from unittest.mock import Mock
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.application.usecases.appliance.network_interfaces.set_description_network_interface import \
    SetDescriptionNetworkInterface
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class TestSetDescriptionNetworkInterface:
    @staticmethod
    def test_return_network_interface_when_set_description_is_called_with_valid_interface_and_description():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_description.return_value = NetworkInterface(**{"name": "Ethernet0/0", "description": "",
                                                                          "macAddress": "aabb.cc00.0100",
                                                                          "ipAddress": "unassigned", "mtu": 1500,
                                                                          "status": "up",
                                                                          "protocol": "up"})

        usecase = SetDescriptionNetworkInterface(mock_appliance)
        result = usecase.set_description("valid_interface", "valid_description")

        assert isinstance(result, NetworkInterface)

    @staticmethod
    def test_raise_exception_when_set_description_is_called_with_invalid_interface():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_description.side_effect = Exception

        usecase = SetDescriptionNetworkInterface(mock_appliance)

        try:
            usecase.set_description("invalid_interface", "valid_description")
            assert False
        except Exception:
            assert True

    @staticmethod
    def test_return_none_when_set_description_is_called_with_no_interface():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_description.return_value = None

        usecase = SetDescriptionNetworkInterface(mock_appliance)
        result = usecase.set_description(None, "valid_description")

        assert result is None
    @staticmethod
    def test_return_none_when_set_description_is_called_with_no_description():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_description.return_value = None

        usecase = SetDescriptionNetworkInterface(mock_appliance)
        result = usecase.set_description("valid_interface", None)

        assert result is None
