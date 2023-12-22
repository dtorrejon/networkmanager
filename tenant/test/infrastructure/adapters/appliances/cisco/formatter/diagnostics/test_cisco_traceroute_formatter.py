import pytest
from tenant.infraestructure.adapters.appliances.cisco.formatter.diagnostics.cisco_ios_traceroute_formatter import \
    CiscoIosTraceRouteFormatter
from tenant.domain.schemas.appliances.diagnostics.trace_route import TraceRoute
from tenant.domain.schemas.appliances.diagnostics.trace_route_command_fields import TraceRouteCommandFields


class TestCiscoIosTraceRouteFormatter:
    @staticmethod
    def test_format_valid_traceroute_text():
        traceroute_formatter = CiscoIosTraceRouteFormatter()
        traceroute_text = """
        Type escape sequence to abort.
            Tracing the route to 8.8.4.4
            VRF info: (vrf in name/id, vrf out name/id)
              1 192.168.20.1 6 msec 8 msec 5 msec
              2  * 
                192.168.4.1 17 msec 44 msec
              3 192.168.1.1 21 msec 20 msec 21 msec
              4 81.46.38.215 45 msec 66 msec 36 msec
              5 81.46.44.237 [MPLS: Label 8602 Exp 0] 59 msec 71 msec 30 msec
              6 81.46.45.33 [MPLS: Label 5961 Exp 0] 51 msec *  61 msec
              7  * 
                80.58.106.1 37 msec * 
              8 176.52.253.97 41 msec 54 msec 48 msec
              9 5.53.1.74 30 msec
                5.53.0.110 84 msec
                176.52.253.102 32 msec
             10 74.125.242.177 52 msec 38 msec
                108.170.253.225 45 msec
             11 142.251.54.149 29 msec
                142.250.232.7 37 msec
                142.250.213.125 28 msec
             12 8.8.8.8 29 msec 48 msec 52 msec
             13 192.168.4.1 17 msec 15 msec 19 msec
             14 192.168.1.1 35 msec 23 msec 18 msec
             15 81.46.38.215 19 msec 23 msec 26 msec
             16 81.46.44.233 [MPLS: Label 8664 Exp 0] 29 msec 29 msec 29 msec
             17  *  *  * 
             18  *  *  * 
             19  *  *  * 
             20 209.85.149.88 34 msec
                5.53.0.110 34 msec
                209.85.149.88 44 msec
             21 108.170.253.225 34 msec
                108.170.253.241 34 msec
                108.170.253.225 28 msec
             22 74.125.253.199 31 msec
                142.250.232.7 30 msec
                142.250.232.11 26 msec
             23  *  * 
                80.58.106.1 37 msec
             24 8.8.4.4 33 msec 32 msec 28 msec"""

        command_fields = TraceRouteCommandFields(destinationIpAddress="192.168.1.1", probeCount=3)
        result = traceroute_formatter.format(traceroute_text, command_fields)
        assert isinstance(result, TraceRoute)
        assert len(result.hops) == 24
        assert result.hops[0].hopNumber == "1"
        assert result.hops[0].probeCount[0].time == "6"
        assert result.hops[1].hopNumber == "2"
        assert result.hops[1].probeCount[1].time == "17"
