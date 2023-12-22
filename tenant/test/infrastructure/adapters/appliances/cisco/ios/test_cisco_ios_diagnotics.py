import pytest
from unittest.mock import Mock, patch
from tenant.infraestructure.adapters.appliances.cisco.ios.cisco_ios_diagnotics import CiscoIosDiagnostics
from tenant.domain.schemas.appliances.diagnostics.trace_route_command_fields import TraceRouteCommandFields
from tenant.domain.schemas.appliances.diagnostics.trace_route import TraceRoute
class TestCiscoIosDiagnostics:

    return_value = """
        Type escape sequence to abort.
Tracing the route to 8.8.8.8
VRF info: (vrf in name/id, vrf out name/id)
  1 192.168.20.1 4 msec 5 msec 8 msec
  2 192.168.4.1 54 msec 21 msec 11 msec
  3 192.168.1.1 15 msec 21 msec 19 msec
  4 81.46.38.215 17 msec 19 msec 18 msec
  5 81.46.44.237 [MPLS: Label 8602 Exp 0] 30 msec 29 msec 27 msec
  6 81.46.45.33 [MPLS: Label 5961 Exp 0] 24 msec 26 msec
    80.58.106.14 [MPLS: Label 514474 Exp 0] 24 msec
  7  *  *  * 
  8  *  * 
    176.52.253.97 43 msec
  9 5.53.0.110 35 msec 31 msec 28 msec
 10 108.170.253.225 29 msec 26 msec
    74.125.242.161 24 msec
 11 142.250.213.125 25 msec
    142.251.49.55 28 msec
    142.250.46.165 26 msec
 12 8.8.8.8 25 msec 25 msec 30 msec"""
    @classmethod
    @patch('netmiko.BaseConnection')
    def test_traceroute(cls, mock_connection):
        mock_connection.host = "192.168.1.1"
        mock_connection.password = "password"
        mock_connection.send_command_timing.return_value = cls.return_value
        diagnostics = CiscoIosDiagnostics(mock_connection)
        trace_route_command_fields = TraceRouteCommandFields(destinationIpAddress="192.168.1.2", sourceIpAddress=None, probeCount=3)
        result = diagnostics.traceroute(trace_route_command_fields)
        assert isinstance(result, TraceRoute)
    @classmethod
    @patch('netmiko.BaseConnection')
    def test_traceroute_with_source_ip(cls, mock_connection):
        mock_connection.host = "192.168.1.1"
        mock_connection.password = "password"
        mock_connection.send_command_timing.return_value = cls.return_value
        diagnostics = CiscoIosDiagnostics(mock_connection)
        trace_route_command_fields = TraceRouteCommandFields(destinationIpAddress="192.168.1.2", sourceIpAddress="192.168.1.3", probeCount=3)
        result = diagnostics.traceroute(trace_route_command_fields)
        assert isinstance(result, TraceRoute)