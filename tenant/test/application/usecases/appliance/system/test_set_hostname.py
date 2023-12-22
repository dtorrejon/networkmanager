from unittest.mock import Mock
from tenant.application.usecases.appliance.system.set_hostname import SetHostname
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance
from tenant.domain.schemas.appliances.system.hostname import Hostname

class TestSetHostname:

    @staticmethod
    def test_return_hostname_when_set_hostname_is_called_with_valid_hostname():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_hostname.return_value = Hostname(**{
                    "status": "ok",
                    "message": "New hostname switch01, successfully updated"
                })

        usecase = SetHostname(mock_appliance)
        result = usecase.set_hostname("valid_hostname")

        assert isinstance(result, Hostname)
    @staticmethod
    def test_raise_exception_when_set_hostname_is_called_with_invalid_hostname():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_hostname.side_effect = Exception

        usecase = SetHostname(mock_appliance)

        try:
            usecase.set_hostname("invalid_hostname")
            assert False
        except Exception:
            assert True
    @staticmethod
    def test_return_none_when_set_hostname_is_called_with_no_hostname():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.set_hostname.return_value = None

        usecase = SetHostname(mock_appliance)
        result = usecase.set_hostname(None)

        assert result is None
