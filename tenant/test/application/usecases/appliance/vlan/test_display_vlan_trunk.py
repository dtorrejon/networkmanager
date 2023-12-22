from unittest.mock import Mock
from tenant.application.usecases.appliance.vlan.display_vlan_trunk import DisplayVlanTrunk
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance
from tenant.domain.schemas.appliances.vlans.vlan_trunk import VlanTrunk


class TestDisplayVlanTrunk:
    @staticmethod
    def test_return_vlan_trunk_list_when_display_is_called():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.display_vlan_trunk.return_value = [VlanTrunk(**{
            "port": "Et1/2",
            "mode": "on",
            "encapsulation": "802.1q",
            "status": "trunking",
            "nativeVlan": 1,
            "allowedTrunkVlans": [
                701,
                702,
                703,
                704
            ]
        })]

        usecase = DisplayVlanTrunk(mock_appliance)
        result = usecase.display()

        assert len(result) > 0
        assert isinstance(result[0], VlanTrunk)

    @staticmethod
    def test_raise_exception_when_display_is_called_and_appliance_raises_exception():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.display_vlan_trunk.side_effect = Exception

        usecase = DisplayVlanTrunk(mock_appliance)

        try:
            usecase.display()
            assert False
        except Exception:
            assert True

    @staticmethod
    def test_return_empty_list_when_display_is_called_and_appliance_returns_empty_list():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.display_vlan_trunk.return_value = []

        usecase = DisplayVlanTrunk(mock_appliance)
        result = usecase.display()

        assert len(result) == 0
