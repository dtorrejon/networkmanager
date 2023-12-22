from unittest.mock import Mock
from tenant.application.usecases.appliance.svi.delete_svi import DeleteSVI
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface


class TestDeleteSVI:
    @staticmethod
    def test_return_network_interface_list_when_delete_is_called_with_valid_vlan_id():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.delete_svi.return_value = [NetworkInterface(**{"name": "vlan60", "description": "",
                                                                      "macAddress": "aabb.cc00.0100",
                                                                      "ipAddress": "unassigned", "mtu": 1500,
                                                                      "status": "up",
                                                                      "protocol": "up"})]

        usecase = DeleteSVI(mock_appliance)
        result = usecase.delete("valid_vlan_id")

        assert len(result) > 0
        assert isinstance(result[0], NetworkInterface)

    @staticmethod
    def test_raise_exception_when_delete_is_called_with_invalid_vlan_id():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.delete_svi.side_effect = Exception

        usecase = DeleteSVI(mock_appliance)

        try:
            usecase.delete("invalid_vlan_id")
            assert False
        except Exception:
            assert True

    @staticmethod
    def test_return_empty_list_when_delete_is_called_with_no_vlan_id():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.delete_svi.return_value = []

        usecase = DeleteSVI(mock_appliance)
        result = usecase.delete(None)

        assert len(result) == 0
