from unittest.mock import Mock
from tenant.application.usecases.appliance.status.read_node_status import ReadNodeStatus
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class TestReadNodeStatus:
    @staticmethod
    def test_return_true_when_read_is_called_and_service_status_is_true():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.service_status.return_value = True

        usecase = ReadNodeStatus(mock_appliance)
        result = usecase.read()

        assert result is True

    @staticmethod
    def test_return_false_when_read_is_called_and_service_status_is_false():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.service_status.return_value = False

        usecase = ReadNodeStatus(mock_appliance)
        result = usecase.read()

        assert result is False

    @staticmethod
    def test_raise_exception_when_read_is_called_and_service_status_raises_exception():
        mock_appliance = Mock(spec=Appliance)
        mock_appliance.service_status.side_effect = Exception

        usecase = ReadNodeStatus(mock_appliance)

        try:
            usecase.read()
            assert False
        except Exception:
            assert True
