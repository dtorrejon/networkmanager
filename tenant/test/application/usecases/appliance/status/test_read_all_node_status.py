from unittest.mock import Mock
from tenant.application.usecases.appliance.status.read_all_node_status import ReadAllNodeStatus
from tenant.infraestructure.gateways.appliance.interface_appliance_status import IApplianceStatus


class TestReadAllNodeStatus:

    @staticmethod
    def test_return_all_node_status_when_read_all_is_called():
        mock_appliance_status = Mock(spec=IApplianceStatus)
        mock_appliance_status.get_all.return_value = {"node1": "status1", "node2": "status2"}

        usecase = ReadAllNodeStatus(mock_appliance_status)
        result = usecase.read_all()

        assert len(result) == 2
        assert result["node1"] == "status1"
        assert result["node2"] == "status2"

    @staticmethod
    def test_raise_exception_when_read_all_is_called_and_appliance_status_raises_exception():
        mock_appliance_status = Mock(spec=IApplianceStatus)
        mock_appliance_status.get_all.side_effect = Exception

        usecase = ReadAllNodeStatus(mock_appliance_status)

        try:
            usecase.read_all()
            assert False
        except Exception:
            assert True

    @staticmethod
    def test_return_empty_dict_when_read_all_is_called_and_appliance_status_returns_empty_dict():
        mock_appliance_status = Mock(spec=IApplianceStatus)
        mock_appliance_status.get_all.return_value = {}

        usecase = ReadAllNodeStatus(mock_appliance_status)
        result = usecase.read_all()

        assert len(result) == 0
