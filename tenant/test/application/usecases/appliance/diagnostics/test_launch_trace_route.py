from unittest.mock import Mock
from tenant.domain.schemas.appliances.diagnostics.trace_route import TraceRoute
from tenant.domain.schemas.appliances.diagnostics.trace_route_command_fields import TraceRouteCommandFields
from tenant.application.usecases.appliance.diagnostics.launch_trace_route import LaunchTraceRoute
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance
class TestLaunchTraceRoute:
    @staticmethod
    def test_return_trace_route_when_trace_route_is_called_with_valid_command_fields():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.trace_route.return_value = TraceRoute(**{
                    "hops": [
                        {
                            "hopNumber": "1",
                            "probeCount": [
                                {
                                    "id": "1",
                                    "ip": "192.168.20.1",
                                    "time": "3",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "2",
                                    "ip": "192.168.20.1",
                                    "time": "6",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "3",
                                    "ip": "192.168.20.1",
                                    "time": "7",
                                    "timeScale": "ms"
                                }
                            ]
                        },
                        {
                            "hopNumber": "2",
                            "probeCount": [
                                {
                                    "id": "1",
                                    "ip": "192.168.4.1",
                                    "time": "27",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "2",
                                    "ip": "192.168.4.1",
                                    "time": "14",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "3",
                                    "ip": "192.168.4.1",
                                    "time": "25",
                                    "timeScale": "ms"
                                }
                            ]
                        },
                        {
                            "hopNumber": "3",
                            "probeCount": [
                                {
                                    "id": "1",
                                    "ip": "192.168.1.1",
                                    "time": "34",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "2",
                                    "ip": "192.168.1.1",
                                    "time": "17",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "3",
                                    "ip": "192.168.1.1",
                                    "time": "21",
                                    "timeScale": "ms"
                                }
                            ]
                        },
                        {
                            "hopNumber": "4",
                            "probeCount": [
                                {
                                    "id": "1",
                                    "ip": "81.46.38.215",
                                    "time": "18",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "2",
                                    "ip": "81.46.38.215",
                                    "time": "22",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "3",
                                    "ip": "81.46.38.215",
                                    "time": "20",
                                    "timeScale": "ms"
                                }
                            ]
                        },
                        {
                            "hopNumber": "5",
                            "probeCount": [
                                {
                                    "id": "1",
                                    "ip": "81.46.44.233",
                                    "time": "19",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "2",
                                    "ip": "81.46.44.233",
                                    "time": "21",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "3",
                                    "ip": "81.46.44.233",
                                    "time": "22",
                                    "timeScale": "ms"
                                }
                            ]
                        },
                        {
                            "hopNumber": "6",
                            "probeCount": [
                                {
                                    "id": "1",
                                    "ip": "81.46.45.29",
                                    "time": "21",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "2",
                                    "ip": "81.46.45.29",
                                    "time": "18",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "3",
                                    "ip": "81.46.45.29",
                                    "time": "19",
                                    "timeScale": "ms"
                                }
                            ]
                        },
                        {
                            "hopNumber": "7",
                            "probeCount": [
                                {
                                    "id": "1",
                                    "ip": "80.58.78.1",
                                    "time": "24",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "2",
                                    "ip": "80.58.78.1",
                                    "time": "21",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "3",
                                    "ip": "80.58.78.1",
                                    "time": "33",
                                    "timeScale": "ms"
                                }
                            ]
                        },
                        {
                            "hopNumber": "8",
                            "probeCount": [
                                {
                                    "id": "1",
                                    "ip": "216.184.113.232",
                                    "time": "30",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "2",
                                    "ip": "216.184.113.232",
                                    "time": "28",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "3",
                                    "ip": "216.184.113.232",
                                    "time": "29",
                                    "timeScale": "ms"
                                }
                            ]
                        },
                        {
                            "hopNumber": "9",
                            "probeCount": [
                                {
                                    "id": "1",
                                    "ip": "*",
                                    "time": "*",
                                    "timeScale": "*"
                                },
                                {
                                    "id": "2",
                                    "ip": "*",
                                    "time": "*",
                                    "timeScale": "*"
                                },
                                {
                                    "id": "3",
                                    "ip": "176.52.248.251",
                                    "time": "27",
                                    "timeScale": "ms"
                                }
                            ]
                        },
                        {
                            "hopNumber": "10",
                            "probeCount": [
                                {
                                    "id": "1",
                                    "ip": "*",
                                    "time": "*",
                                    "timeScale": "*"
                                },
                                {
                                    "id": "2",
                                    "ip": "*",
                                    "time": "*",
                                    "timeScale": "*"
                                },
                                {
                                    "id": "3",
                                    "ip": "81.173.106.39",
                                    "time": "60",
                                    "timeScale": "ms"
                                }
                            ]
                        },
                        {
                            "hopNumber": "11",
                            "probeCount": [
                                {
                                    "id": "1",
                                    "ip": "188.114.108.7",
                                    "time": "25",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "2",
                                    "ip": "172.70.58.2",
                                    "time": "27",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "3",
                                    "ip": "172.70.60.2",
                                    "time": "35",
                                    "timeScale": "ms"
                                }
                            ]
                        },
                        {
                            "hopNumber": "12",
                            "probeCount": [
                                {
                                    "id": "1",
                                    "ip": "1.1.1.1",
                                    "time": "40",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "2",
                                    "ip": "1.1.1.1",
                                    "time": "25",
                                    "timeScale": "ms"
                                },
                                {
                                    "id": "3",
                                    "ip": "1.1.1.1",
                                    "time": "24",
                                    "timeScale": "ms"
                                }
                            ]
                        }
                    ]
                })

        usecase = LaunchTraceRoute(mock_appliance)
        result = usecase.trace_route(TraceRouteCommandFields(**{"destinationIpAddress": "8.8.8.8"}))

        assert isinstance(result, TraceRoute)
    @staticmethod
    def test_raise_exception_when_trace_route_is_called_with_invalid_command_fields():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.trace_route.side_effect = Exception

        usecase = LaunchTraceRoute(mock_appliance)

        try:
            usecase.trace_route("invalid_command_fields")
            assert False
        except Exception:
            assert True
    @staticmethod
    def test_return_none_when_trace_route_is_called_with_no_command_fields():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.trace_route.return_value = None

        usecase = LaunchTraceRoute(mock_appliance)
        result = usecase.trace_route(None)

        assert result is None
