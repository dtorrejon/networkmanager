from unittest.mock import patch

from tenant.domain.schemas.appliances.vlans.vlan_brief import VlanBrief
from tenant.domain.schemas.appliances.vlans.vlan_resume import VlanResume
from tenant.domain.schemas.appliances.vlans.vlan_trunk import VlanTrunk
from tenant.infraestructure.adapters.appliances.cisco.ios.cisco_ios_vlan import CiscoIosVlan
class TestCiscoIosVlan:

    @staticmethod
    @patch('netmiko.BaseConnection')
    def test_display_vlan_brief_returns_expected_result(MockBaseConnection):
        mock_connection = MockBaseConnection()
        mock_connection.send_command_timing.return_value = """
VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Et0/0, Et0/1, Et0/3, Et1/0, Et1/1, Et1/3
99   VLAN0099                         active    
789  VLAN0789                         active    Et3/1
1002 fddi-default                     act/unsup 
1003 token-ring-default               act/unsup 
1004 fddinet-default                  act/unsup 
1005 trnet-default                    act/unsup"""
        system = CiscoIosVlan(mock_connection)
        result = system.display_vlan_brief()
        assert isinstance(result, list)
        assert isinstance(result[0], VlanBrief)
    @staticmethod
    @patch('netmiko.BaseConnection')
    def test_et_vlan_access_sets_correct_vlan(MockBaseConnection):
        mock_connection = MockBaseConnection()
        mock_connection.send_command_timing.return_value = """
        VLAN Name                             Status    Ports
        ---- -------------------------------- --------- -------------------------------
        1    default                          active    Et0/0, Et0/1, Et0/3, Et1/0, Et1/1, Et1/3
        99   VLAN0099                         active    
        789  VLAN0789                         active    Et3/1
        1002 fddi-default                     act/unsup 
        1003 token-ring-default               act/unsup 
        1004 fddinet-default                  act/unsup 
        1005 trnet-default                    act/unsup"""
        system = CiscoIosVlan(mock_connection)
        result = system.set_vlan_access("Ethernet0/1", 10, "dot1q")
        assert isinstance(result, list)
        assert isinstance(result[0], VlanBrief)
    @staticmethod
    @patch('netmiko.BaseConnection')
    def test_set_vlan_trunk_sets_correct_vlan(MockBaseConnection):
        mock_connection = MockBaseConnection()
        mock_connection.send_command_timing.return_value = """
Port        Mode             Encapsulation  Status        Native vlan
Et1/2       on               802.1q         trunking      1
Et2/0       on               802.1q         trunking      1
Et2/1       on               802.1q         trunking      10
Et2/2       on               802.1q         trunking      1
Et2/3       on               802.1q         trunking      1
Et3/0       on               802.1q         trunking      1
Et3/2       on               802.1q         trunking      200
Et3/3       on               802.1q         trunking      200

Port        Vlans allowed on trunk
Et1/2       701-704
Et2/0       50,60,70,80
Et2/1       none
Et2/2       50,60,70,80
Et2/3       501-503
Et3/0       200-206
Et3/2       none
Et3/3       701-704

Port        Vlans allowed and active in management domain
Et1/2       none
Et2/0       none
Et2/1       none
Et2/2       none
Et2/3       none
Et3/0       none
Et3/2       none
Et3/3       none

Port        Vlans in spanning tree forwarding state and not pruned
Et1/2       none
Et2/0       none
Et2/1       none
Et2/2       none
Et2/3       none
Et3/0       none
Et3/2       none
Et3/3       none"""
        system = CiscoIosVlan(mock_connection)
        result = system.set_vlan_trunk("FastEthernet0/1", [10, 20], "dot1q")
        assert isinstance(result, list)
        assert isinstance(result[0], VlanTrunk)
