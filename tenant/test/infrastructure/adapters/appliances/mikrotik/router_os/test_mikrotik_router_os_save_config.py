import unittest
from unittest.mock import patch

from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.infraestructure.adapters.appliances.mikrotik.router_os.mikrotik_router_os_routes import \
    MikrotikRouterOSRoutes
from tenant.infraestructure.adapters.appliances.mikrotik.router_os.mikrotik_router_os_save_config import \
    MikrotikRouterOSSaveConfig


class TestRouterOSSaveConfig(unittest.TestCase):
    def setUp(self):
        self.node = NodeWithCredentials(ipAddress='192.168.1.1', port=80, username='admin', password='password',
                                   name="testswitch", technology="switchl3", vendor="mikrotik", model="RouterOS",
                                   softwareVersion="roureros7.8", protocol="api")

    @patch('requests.request')
    def test_should_save_config_when_called(self, mock_request):
        save_config = MikrotikRouterOSSaveConfig(self.node)
        mock_request.return_value.status_code = 200

        result = save_config._MikrotikRouterOSSaveConfig__save_config()

        self.assertEqual(result, "config saved")


