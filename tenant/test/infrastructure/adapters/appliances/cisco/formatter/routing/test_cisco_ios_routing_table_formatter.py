import pytest
from tenant.infraestructure.adapters.appliances.cisco.formatter.rotuing.cisco_ios_routing_table_formatter import \
    CiscoIosRoutingTableFormatter
from tenant.domain.schemas.appliances.diagnostics.route import Route


class TestCiscoIosRoutingTableFormatter:
    @staticmethod
    def test_format_valid_routing_table_text():
        formatter = CiscoIosRoutingTableFormatter()
        output_text_1 = """
              Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
             D - EIGRP
             EX - EIGRP external
              O - OSPF, IA - OSPF inter area 
             N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
             E1 - OSPF external type 1, E2 - OSPF external type 2
             i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
             ia - IS-IS inter area, * - candidate default, U - per-user static route
             o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
             a - application route
             + - replicated route, % - next hop override

      Gateway of last resort is not set

            2.0.0.0/32 is subnetted, 1 subnets
      C        2.2.2.2 is directly connected, Loopback0
            3.0.0.0/32 is subnetted, 1 subnets
      D        3.3.3.3 [90/409600] via 192.168.23.3, 02:01:14, Ethernet0/1
            4.0.0.0/32 is subnetted, 1 subnets
      D        4.4.4.4 [90/435200] via 192.168.23.3, 02:01:00, Ethernet0/1
            192.168.12.0/24 is variably subnetted, 2 subnets, 2 masks
      C        192.168.12.0/24 is directly connected, Ethernet0/2
      L        192.168.12.2/32 is directly connected, Ethernet0/2
            192.168.23.0/24 is variably subnetted, 2 subnets, 2 masks
      C        192.168.23.0/24 is directly connected, Ethernet0/1
      L        192.168.23.2/32 is directly connected, Ethernet0/1
      D     192.168.34.0/24 [90/307200] via 192.168.23.3, 02:01:14, Ethernet0/1
              """
        output_text_2 = """
              Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
             D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
             N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
             E1 - OSPF external type 1, E2 - OSPF external type 2
             i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
             ia - IS-IS inter area, * - candidate default, U - per-user static route
             o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
             a - application route
             + - replicated route, % - next hop override, p - overrides from PfR

      Gateway of last resort is not set

            192.168.10.0/24 is variably subnetted, 2 subnets, 2 masks
      C        192.168.10.0/24 is directly connected, GigabitEthernet0/1.10
      L        192.168.10.1/32 is directly connected, GigabitEthernet0/1.10
            192.168.20.0/24 is variably subnetted, 2 subnets, 2 masks
      C        192.168.20.0/24 is directly connected, GigabitEthernet0/1.20
      L        192.168.20.1/32 is directly connected, GigabitEthernet0/1.20
            192.168.56.0/24 is variably subnetted, 2 subnets, 2 masks
      C        192.168.56.0/24 is directly connected, GigabitEthernet0/1.56
      L        192.168.56.1/32 is directly connected, GigabitEthernet0/1.56
            192.168.98.0/24 is variably subnetted, 2 subnets, 2 masks
      C        192.168.98.0/24 is directly connected, GigabitEthernet0/1.98
      L        192.168.98.1/32 is directly connected, GigabitEthernet0/1.98
            192.168.100.0/24 is variably subnetted, 2 subnets, 2 masks
      C        192.168.100.0/24 is directly connected, GigabitEthernet0/1.100
      L        192.168.100.1/32 is directly connected, GigabitEthernet0/1.100
              """
        output_text_3 = """
              Codes: C - connected, S - static, I - IGRP, R - RIP, M - mobile, B - BGP
             D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
             E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
             i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, * - candidate default

      Gateway of last resort is not set

      S    134.134.0.0 is directly connected, Ethernet0
      S    131.131.0.0 is directly connected, Ethernet0
      S    129.129.0.0 is directly connected, Ethernet0
      S    128.128.0.0 is directly connected, Ethernet0
      S    198.49.246.0 is directly connected, Ethernet0
      S    192.160.97.0 is directly connected, Ethernet0
      S    192.153.88.0 is directly connected, Ethernet0
      S    192.76.141.0 is directly connected, Ethernet0
      S    192.75.138.0 is directly connected, Ethernet0
      S    192.44.237.0 is directly connected, Ethernet0
      S    192.31.222.0 is directly connected, Ethernet0
      S    192.16.209.0 is directly connected, Ethernet0
      S    144.145.0.0 is directly connected, Ethernet0
      S    140.141.0.0 is directly connected, Ethernet0
      S    139.138.0.0 is directly connected, Ethernet0
      S    129.128.0.0 is directly connected, Ethernet0
           172.19.0.0 255.255.255.0 is subnetted, 1 subnets
      C       172.19.64.0 is directly connected, Ethernet0
           171.69.0.0 is variably subnetted, 2 subnets, 2 masks
      C       171.69.232.32 255.255.255.240 is directly connected, Ethernet0
      S       171.69.0.0 255.255.0.0 is directly connected, Ethernet0
              """
        output_text_4 = """
              Codes: I - IGRP derived, R - RIP derived, O - OSPF derived
             C - connected, S - static, E - EGP derived, B - BGP derived
             i - IS-IS derived
             * - candidate default route, IA - OSPF inter area route
      	E1 - OSPF external type 1 route, E2 - OSPF external type 2 route
             L1 - IS-IS level-1 route, L2 - IS-IS level-2 route
      Gateway of last resort is not set
           160.89.0.0 is subnetted (mask is 255.255.255.0), 3 subnets
      C       160.89.64.0 255.255.255.0 is possibly down,
                routing via 0.0.0.0, Ethernet0
      i L2    160.89.67.0 [115/20] via 160.89.64.240, 0:00:12, Ethernet0
      i L2    160.89.66.0 [115/20] via 160.89.64.240, 0:00:12, Ethernet0
              """
        output_text_5 = """
              Codes: I - IGRP derived, R - RIP derived, O - OSPF derived
             C - connected, S - static, E - EGP derived, B - BGP derived
             * - candidate default route, IA - OSPF inter area route
             E1 - OSPF external type 1 route, E2 - OSPF external type 2 route
      Gateway of last resort is 131.119.254.240 to network 129.140.0.0
      O E2 150.150.0.0 [160/5] via 131.119.254.6, 0:01:00, Ethernet2
      E    192.67.131.0 [200/128] via 131.119.254.244, 0:02:22, Ethernet2
      O E2 192.68.132.0 [160/5] via 131.119.254.6, 0:00:59, Ethernet2
      O E2 130.130.0.0 [160/5] via 131.119.254.6, 0:00:59, Ethernet2
      E    128.128.0.0 [200/128] via 131.119.254.244, 0:02:22, Ethernet2
      E    129.129.0.0 [200/129] via 131.119.254.240, 0:02:22, Ethernet2
      E    192.65.129.0 [200/128] via 131.119.254.244, 0:02:22, Ethernet2
      E    131.131.0.0 [200/128] via 131.119.254.244, 0:02:22, Ethernet2
      E    192.75.139.0 [200/129] via 131.119.254.240, 0:02:23, Ethernet2
      E    192.16.208.0 [200/128] via 131.119.254.244, 0:02:22, Ethernet2
      E    192.84.148.0 [200/129] via 131.119.254.240, 0:02:23, Ethernet2
      E    192.31.223.0 [200/128] via 131.119.254.244, 0:02:22, Ethernet2
      E    192.44.236.0 [200/129] via 131.119.254.240, 0:02:23, Ethernet2
      E    140.141.0.0 [200/129] via 131.119.254.240, 0:02:22, Ethernet2
      E    141.140.0.0 [200/129] via 131.119.254.240, 0:02:23, Ethernet2
      """
        result = formatter.format(output_text_1)
        assert len(result) == 8
        assert isinstance(result[0], Route)
        assert result[0].destination == "2.2.2.2"
        assert result[0].protocol == "CONNECTED"
        assert result[0].preference == 0
        assert result[0].cost == 0
        assert result[0].nextHop == "directly"
        assert result[0].interface == "Loopback0"
        assert result[0].age == "-"

    @staticmethod
    def test_format_routing_table_text_empty():
        formatter = CiscoIosRoutingTableFormatter()
        routing_table_text = ""
        result = formatter.format(routing_table_text)
        assert result == []

    @staticmethod
    def test_format_routing_table_text_no_routes():
        formatter = CiscoIosRoutingTableFormatter()
        routing_table_text = "Gateway of last resort is not set"
        result = formatter.format(routing_table_text)
        assert result == []
