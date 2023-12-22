from unittest.mock import Mock
from tenant.domain.schemas.appliances.diagnostics.route import Route
from tenant.application.usecases.appliance.routing.set_default_gateway import SetDefaultGateway
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class TestSetDefaultGateway:

    @staticmethod
    def test_return_route_list_when_set_default_gateway_is_called_with_valid_ip():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_default_gateway.return_value = [Route(**{
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

        usecase = SetDefaultGateway(mock_appliance)
        result = usecase.set_default_gateway("ip")

        assert len(result) > 0
        assert isinstance(result[0], Route)

    @staticmethod
    def test_raise_exception_when_set_default_gateway_is_called_with_invalid_ip():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_default_gateway.side_effect = Exception

        usecase = SetDefaultGateway(mock_appliance)

        try:
            usecase.set_default_gateway("invalid_ip")
            assert False
        except Exception:
            assert True
