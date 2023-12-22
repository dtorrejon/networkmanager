from unittest.mock import Mock
from tenant.application.usecases.appliance.svi.create_svi import CreateSVI
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface


class TestCreateSVI:

    @staticmethod
    def test_return_network_interface_when_create_is_called_with_valid_vlan_id():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.create_svi.return_value = NetworkInterface(**{"name": "vlan60", "description": "",
                                                                     "macAddress": "aabb.cc00.0100",
                                                                     "ipAddress": "unassigned", "mtu": 1500,
                                                                     "status": "up",
                                                                     "protocol": "up"})

        usecase = CreateSVI(mock_appliance)
        result = usecase.create("valid_vlan_id")

        assert isinstance(result, NetworkInterface)

    @staticmethod
    def test_raise_exception_when_create_is_called_with_invalid_vlan_id():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.create_svi.side_effect = Exception

        usecase = CreateSVI(mock_appliance)

        try:
            usecase.create("invalid_vlan_id")
            assert False
        except Exception:
            assert True

    @staticmethod
    def test_return_none_when_create_is_called_with_no_vlan_id():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.create_svi.return_value = None

        usecase = CreateSVI(mock_appliance)
        result = usecase.create(None)

        assert result is None
