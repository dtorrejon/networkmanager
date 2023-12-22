import unittest
from unittest.mock import patch

from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.infraestructure.adapters.appliances.mikrotik.router_os.mikrotik_router_os_routes import \
    MikrotikRouterOSRoutes


class TestMikrotikRouterOSRoutes(unittest.TestCase):

    def setUp(self):
        self.node = NodeWithCredentials(ipAddress='192.168.1.1', port=80, username='admin', password='password',
                                   name="testswitch", technology="switchl3", vendor="mikrotik", model="RouterOS",
                                   softwareVersion="roureros7.8", protocol="api")
    @patch('requests.request')
    def test_should_return_routing_table_when_called(self, mock_request):
        routes = MikrotikRouterOSRoutes(self.node)
        mock_request.return_value.json.return_value = [
            {'dst-address': '192.168.1.0/24', 'gateway': '192.168.1.1', 'scope': '30', 'distance': '1', 'local-address': 'eth1'},
            {'dst-address': '192.168.2.0/24', 'gateway': '192.168.2.1', 'scope': '30', 'distance': '1', 'local-address': 'eth2'}]

        result = routes.routing_table()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].destination, '192.168.1.0/24')
        self.assertEqual(result[0].nextHop, 'eth1')
        self.assertEqual(result[0].interface, '192.168.1.1')
        self.assertEqual(result[1].destination, '192.168.2.0/24')
        self.assertEqual(result[1].nextHop, 'eth2')
        self.assertEqual(result[1].interface, '192.168.2.1')

    @patch('requests.request')
    def test_should_set_default_gateway_when_called(self, mock_request):
        routes = MikrotikRouterOSRoutes(self.node)
        mock_request.return_value.json.return_value = [
            {'dst-address': '0.0.0.0/0', 'gateway': '192.168.1.1', 'scope': '30', 'distance': '1', 'local-address': 'eth1'}]

        result = routes.set_default_gateway('192.168.1.1')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].destination, '0.0.0.0/0')
        self.assertEqual(result[0].nextHop, 'eth1')
        self.assertEqual(result[0].interface, '192.168.1.1')

    @patch('requests.request')
    def test_should_set_static_route_when_called(self, mock_request):
        routes = MikrotikRouterOSRoutes(self.node)
        mock_request.return_value.json.return_value = [
            {'dst-address': '192.168.3.0/24', 'gateway': '192.168.3.1', 'scope': '30', 'distance': '1',
             'local-address': 'eth3'}]

        result = routes.set_static_route('192.168.3.0/24', '192.168.3.1')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].destination, '192.168.3.0/24')
        self.assertEqual(result[0].nextHop, 'eth3')
        self.assertEqual(result[0].interface, '192.168.3.1')