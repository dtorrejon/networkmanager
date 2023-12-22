from tenant.domain.schemas.appliances.vlans.vlan_brief import VlanBrief
from tenant.infraestructure.adapters.appliances.cisco.formatter.vlan.cisco_ios_display_vlan_brief_formatter import \
    CiscoIosDisplayVlanBriefFormatter


class TestCiscoIosDisplayVlanBriefFormatter:
    @staticmethod
    def test_format_valid_display_text():
        formatter = CiscoIosDisplayVlanBriefFormatter()
        display_text = """
VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Et0/0, Et0/1, Et0/3, Et1/0, Et1/1, Et1/3
99   VLAN0099                         active    
789  VLAN0789                         active    Et3/1
1002 fddi-default                     act/unsup 
1003 token-ring-default               act/unsup 
1004 fddinet-default                  act/unsup 
1005 trnet-default                    act/unsup """

        result = formatter.format(display_text)
        assert len(result) == 7
        assert isinstance(result[0], VlanBrief)
        assert result[0].vlan == 1
        assert result[0].name == "default"
        assert result[0].status == "active"
        assert result[0].ports == ["Et0/0", "Et0/1", "Et0/3", "Et1/0", "Et1/1", "Et1/3"]
        assert isinstance(result[1], VlanBrief)
        assert result[1].vlan == 99
        assert result[1].name == "VLAN0099"
        assert result[1].status == "active"
        assert result[1].ports == []
