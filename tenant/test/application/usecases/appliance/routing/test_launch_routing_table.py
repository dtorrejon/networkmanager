from unittest.mock import Mock
from tenant.domain.schemas.appliances.diagnostics.route import Route
from tenant.application.usecases.appliance.routing.launch_routing_table import LaunchRoutingTable
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class TestLaunchRoutingTable:
    @staticmethod
    def test_return_route_list_when_routing_table_is_called():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.routing_table.return_value = [Route(**{
            "id": 1,
            "destination": "0.0.0.0/0",
            "protocol": "STATIC_CANDIDATE_DEFAULT",
            "preference": 1,
            "cost": 0,
            "nextHop": "192.168.20.1",
            "interface": "192.168.20.1",
            "age": "-"}),

                                                     Route(**{

                                                         "id": 2,
                                                         "destination": "192.168.20.0/24",
                                                         "protocol": "CONNECTED",
                                                         "preference": 0,
                                                         "cost": 0,
                                                         "nextHop": "directly",
                                                         "interface": "Vlan1",
                                                         "age": "-"})]

        usecase = LaunchRoutingTable(mock_appliance)
        result = usecase.routing_table()

        assert len(result) > 0
        assert isinstance(result[0], Route)

    @staticmethod
    def test_raise_exception_when_routing_table_is_called_and_appliance_raises_exception():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.routing_table.side_effect = Exception

        usecase = LaunchRoutingTable(mock_appliance)

        try:
            usecase.routing_table()
            assert False
        except Exception:
            assert True

    @staticmethod
    def test_return_empty_list_when_routing_table_is_called_and_appliance_returns_empty_list():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.routing_table.return_value = []

        usecase = LaunchRoutingTable(mock_appliance)
        result = usecase.routing_table()

        assert len(result) == 0
