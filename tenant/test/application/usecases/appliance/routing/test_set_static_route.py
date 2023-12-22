from unittest.mock import Mock
from tenant.domain.schemas.appliances.diagnostics.route import Route
from tenant.application.usecases.appliance.routing.set_static_route import SetStaticRoute
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class TestSetStaticRoute:
    @staticmethod
    def test_return_route_list_when_set_static_route_is_called_with_valid_ip_and_mask_and_next_hop():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_static_route.return_value = [Route(**{
            "id": 1,
            "destination": "0.0.0.0/0",
            "protocol": "STATIC_CANDIDATE_DEFAULT",
            "preference": 1,
            "cost": 0,
            "nextHop": "192.168.20.1",
            "interface": "192.168.20.1",
            "age": "-"})]

        usecase = SetStaticRoute(mock_appliance)
        result = usecase.set_static_route("valid_ip_and_mask_in_cidr", "valid_ip_next_hop")

        assert len(result) > 0
        assert isinstance(result[0], Route)

    @staticmethod
    def test_raise_exception_when_set_static_route_is_called_with_invalid_ip_and_mask():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_static_route.side_effect = Exception

        usecase = SetStaticRoute(mock_appliance)

        try:
            usecase.set_static_route("invalid_ip_and_mask_in_cidr", "valid_ip_next_hop")
            assert False
        except Exception:
            assert True

    @staticmethod
    def test_return_empty_list_when_set_static_route_is_called_with_no_ip_and_mask():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_static_route.return_value = []

        usecase = SetStaticRoute(mock_appliance)
        result = usecase.set_static_route(None, "valid_ip_next_hop")

        assert len(result) == 0

    @staticmethod
    def test_return_empty_list_when_set_static_route_is_called_with_no_next_hop():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_static_route.return_value = []

        usecase = SetStaticRoute(mock_appliance)
        result = usecase.set_static_route("valid_ip_and_mask_in_cidr", None)

        assert len(result) == 0
