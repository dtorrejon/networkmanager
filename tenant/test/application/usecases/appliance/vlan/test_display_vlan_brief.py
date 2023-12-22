from unittest.mock import Mock
from tenant.application.usecases.appliance.vlan.display_vlan_brief import DisplayVlanBrief
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance
from tenant.domain.schemas.appliances.vlans.vlan_brief import VlanBrief


class TestDisplayVlanBrief:
    @staticmethod
    def test_return_vlan_brief_list_when_display_brief_is_called():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.display_vlan_brief.return_value = [VlanBrief(**{"vlan": 1, "name": "default", "status": "active",
                                                                       "ports": ["Et0/0", "Et0/1", "Et0/3", "Et1/0",
                                                                                 "Et1/1", "Et1/3"]
                                                                       }),
                                                          VlanBrief(**{
                                                              "vlan": 99,
                                                              "name": "VLAN0099",
                                                              "status": "active",
                                                              "ports": []
                                                          })]

        usecase = DisplayVlanBrief(mock_appliance)
        result = usecase.display_brief()

        assert len(result) > 0
        assert isinstance(result[0], VlanBrief)

    @staticmethod
    def test_raise_exception_when_display_brief_is_called_and_appliance_raises_exception():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.display_vlan_brief.side_effect = Exception

        usecase = DisplayVlanBrief(mock_appliance)

        try:
            usecase.display_brief()
            assert False
        except Exception:
            assert True

    @staticmethod
    def test_return_empty_list_when_display_brief_is_called_and_appliance_returns_empty_list():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.display_vlan_brief.return_value = []

        usecase = DisplayVlanBrief(mock_appliance)
        result = usecase.display_brief()

        assert len(result) == 0
