from tenant.domain.ports.appliances.status.interface_read_all_nodes_status import IReadAllNodesStatus
from tenant.infraestructure.gateways.appliance.interface_appliance_status import IApplianceStatus


class ReadAllNodeStatus(IReadAllNodesStatus):

    def __init__(self, appliance_status: IApplianceStatus):
        self.appliance_status = appliance_status

    def read_all(self) -> dict:
        return self.appliance_status.get_all()
