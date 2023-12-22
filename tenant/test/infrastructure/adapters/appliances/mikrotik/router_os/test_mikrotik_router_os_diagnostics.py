import unittest
from unittest.mock import patch, Mock
from tenant.infraestructure.adapters.appliances.mikrotik.router_os.mikrotik_router_os_diagnostics import \
    MikrotikRouterOSDiagnostics
from tenant.domain.schemas.appliances.diagnostics.ping_command_fields import PingCommandFields
from tenant.domain.schemas.appliances.diagnostics.trace_route_command_fields import TraceRouteCommandFields
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials


class TestMikrotikRouterOSDiagnostics(unittest.TestCase):

    def setUp(self):
        self.node = NodeWithCredentials(ipAddress='192.168.1.1', port=80, username='admin', password='password',
                                   name="testswitch", technology="switchl3", vendor="mikrotik", model="RouterOS",
                                   softwareVersion="roureros7.8", protocol="api")
    @patch('requests.request')
    def test_interface_retrieval_with_valid_ip(self, mock_request):
        node = self.node
        diagnostics = MikrotikRouterOSDiagnostics(node)
        mock_request.return_value.json.return_value = [{'address': '192.168.1.2', 'interface': 'eth1'}]

        result = diagnostics.obtain_interface_from_ip('192.168.1.2')

        self.assertEqual(result, 'eth1')

    @patch('requests.request')
    def test_interface_retrieval_with_invalid_ip(self, mock_request):
        node = self.node
        diagnostics = MikrotikRouterOSDiagnostics(node)
        mock_request.return_value.json.return_value = [{'address': '192.168.1.2', 'interface': 'eth1'}]

        result = diagnostics.obtain_interface_from_ip('192.168.1.3')

        self.assertIsNone(result)

    @patch('requests.request')
    def test_successful_ping(self, mock_request):
        node = self.node
        diagnostics = MikrotikRouterOSDiagnostics(node)
        ping_command_fields = PingCommandFields(destinationIpAddress='192.168.1.2', repeat=4)
        mock_request.return_value.json.return_value = [
            {'host': '192.168.1.2', 'sent': '4', 'received': '4', 'min-rtt': '10', 'avg-rtt': '15', 'max-rtt': '20'}]

        result = diagnostics.ping(ping_command_fields)

        self.assertEqual(result.destination, '192.168.1.2')
        self.assertEqual(result.packetsTransmitted, 4)
        self.assertEqual(result.packetsReceived, 4)
        self.assertEqual(result.percent, '100.0%')


    @patch('requests.request')
    def test_successful_traceroute(self, mock_request):
        node = self.node
        diagnostics = MikrotikRouterOSDiagnostics(node)
        trace_route_command_fields = TraceRouteCommandFields(destinationIpAddress='192.168.1.2', probeCount=3)
        mock_request.return_value.json.return_value = [
            {'address': '192.168.1.1', 'last': '10', '.section': '1'},
            {'address': '192.168.1.2', 'last': '20', '.section': '2'},
            {'address': '192.168.1.3', 'last': '30', '.section': '3'}]

        result = diagnostics.traceroute(trace_route_command_fields)
        print(result.model_dump())

        self.assertEqual(len(result.hops), 1)
        self.assertEqual(result.hops[0].hopNumber, '1')
        self.assertEqual(result.hops[0].probeCount[0].ip, '192.168.1.1')
        self.assertEqual(result.hops[0].probeCount[0].time, '10')
        self.assertEqual(result.hops[0].probeCount[0].timeScale, 'ms')

    @patch('requests.request')
    def test_successful_arp(self, mock_request):
        node = self.node
        diagnostics = MikrotikRouterOSDiagnostics(node)
        mock_request.return_value.json.return_value = [
            {'address': '192.168.1.2', 'mac-address': '00:11:22:33:44:55', 'interface': 'eth1'}]

        result = diagnostics.arp()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].ipAddress, '192.168.1.2')
        self.assertEqual(result[0].macAddress, '00:11:22:33:44:55')
        self.assertEqual(result[0].interface, 'eth1')


if __name__ == '__main__':
    unittest.main()
