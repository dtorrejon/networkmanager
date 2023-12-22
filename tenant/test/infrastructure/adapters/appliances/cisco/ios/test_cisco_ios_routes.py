from unittest.mock import patch
from tenant.domain.schemas.appliances.diagnostics.route import Route
from tenant.infraestructure.adapters.appliances.cisco.ios.cisco_ios_routes import CiscoIosStaticRoutes


class TestCiscoIosStaticRoutes:
    routing_table = """
    Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override

Gateway of last resort is 192.168.20.1 to network 0.0.0.0

S*    0.0.0.0/0 [1/0] via 192.168.20.1
      192.168.20.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.20.0/24 is directly connected, Vlan1
L        192.168.20.10/32 is directly connected, Vlan1"""

    @classmethod
    @patch('netmiko.BaseConnection')
    def test_routing_table(cls, mock_connection):
        mock_connection.send_command.return_value = cls.routing_table
        static_routes = CiscoIosStaticRoutes(mock_connection)
        result = static_routes.routing_table()
        assert isinstance(result, list)
        assert all(isinstance(route, Route) for route in result)

    @classmethod
    @patch('netmiko.BaseConnection')
    def test_return_routes_after_setting_default_gateway(cls, mock_connection):
        mock_connection.send_command_timing.return_value = cls.routing_table
        static_routes = CiscoIosStaticRoutes(mock_connection)
        result = static_routes.set_default_gateway("192.168.1.1")
        assert isinstance(result, list)
        assert all(isinstance(route, Route) for route in result)

    @classmethod
    @patch('netmiko.BaseConnection')
    def test_return_routes_after_setting_static_route(cls, mock_connection):
        mock_connection.send_command_timing.return_value = cls.routing_table
        static_routes = CiscoIosStaticRoutes(mock_connection)
        result = static_routes.set_static_route("192.168.1.0/24", "192.168.1.1")
        assert isinstance(result, list)
        assert all(isinstance(route, Route) for route in result)
