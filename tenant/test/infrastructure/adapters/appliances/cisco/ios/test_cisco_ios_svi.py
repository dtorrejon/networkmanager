from unittest.mock import patch

from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.infraestructure.adapters.appliances.cisco.ios.cisco_ios_svi import CiscoIosSvi


class TestCiscoIosSvi:
    vlan_output = """Vlan1 is up, line protocol is up 
  Hardware is Ethernet SVI, address is aabb.cc80.0100 (bia aabb.cc80.0100)
  Description: sw2-uoc-lab
  Internet address is 192.168.20.10/24
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec, 
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive not supported 
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:00:00, output never, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size/max)
  5 minute input rate 2000 bits/sec, 3 packets/sec
  5 minute output rate 1000 bits/sec, 2 packets/sec
     508 packets input, 29095 bytes, 0 no buffer
     Received 10 broadcasts (0 IP multicasts)
     0 runts, 0 giants, 0 throttles 
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     361 packets output, 71753 bytes, 0 underruns
     0 output errors, 0 interface resets
     0 unknown protocol drops
     0 output buffer failures, 0 output buffers swapped out
Vlan120 is administratively down, line protocol is down 
  Hardware is Ethernet SVI, address is aabb.cc80.0100 (bia aabb.cc80.0100)
  Internet address is 192.168.90.4/20
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec, 
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive not supported 
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input never, output never, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size/max)
  5 minute input rate 0 bits/sec, 0 packets/sec
  5 minute output rate 0 bits/sec, 0 packets/sec
     0 packets input, 0 bytes, 0 no buffer
     Received 0 broadcasts (0 IP multicasts)
     0 runts, 0 giants, 0 throttles 
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 packets output, 0 bytes, 0 underruns
     0 output errors, 0 interface resets
     0 unknown protocol drops
     0 output buffer failures, 0 output buffers swapped out
Vlan150 is down, line protocol is down 
  Hardware is Ethernet SVI, address is aabb.cc80.0100 (bia aabb.cc80.0100)
  Internet address is 192.168.120.4/20
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec, 
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive not supported 
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input never, output never, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size/max)
  5 minute input rate 0 bits/sec, 0 packets/sec
  5 minute output rate 0 bits/sec, 0 packets/sec
     0 packets input, 0 bytes, 0 no buffer
     Received 0 broadcasts (0 IP multicasts)
     0 runts, 0 giants, 0 throttles 
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 packets output, 0 bytes, 0 underruns
     0 output errors, 0 interface resets
     0 unknown protocol drops
     0 output buffer failures, 0 output buffers swapped out"""
    @classmethod
    @patch('netmiko.BaseConnection')
    def test_network_interface_after_creating_svi(cls, mock_connection):
        mock_connection.send_command_timing.return_value = cls.vlan_output
        svi = CiscoIosSvi(mock_connection)
        result = svi.create_svi("Vlan1")
        assert isinstance(result, NetworkInterface)
    @classmethod
    @patch('netmiko.BaseConnection')
    def test_network_interface_after_setting_svi_ip(cls, mock_connection):
        mock_connection.send_command_timing.return_value = cls.vlan_output
        svi = CiscoIosSvi(mock_connection)
        result = svi.set_svi_ip("Vlan1", "192.168.1.1/24")
        assert isinstance(result, NetworkInterface)
    @classmethod
    @patch('netmiko.BaseConnection')
    def test_network_interfaces_after_deleting_svi(cls, mock_connection):
        mock_connection.send_command_timing.return_value = cls.vlan_output
        svi = CiscoIosSvi(mock_connection)
        result = svi.delete_svi("Vlan1")
        assert isinstance(result, list)
        assert all(isinstance(interface, NetworkInterface) for interface in result)