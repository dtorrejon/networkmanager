from tenant.domain.ports.appliances.status.interface_read_node_status import IReadNodeStatus
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance



class ReadNodeStatus(IReadNodeStatus):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def read(self) -> bool:
        return self.appliance.service_status()
