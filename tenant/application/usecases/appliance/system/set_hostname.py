from tenant.domain.schemas.appliances.system.hostname import Hostname
from tenant.domain.ports.appliances.system.interface_set_hostname import ISetHostname
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class SetHostname(ISetHostname):

    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def set_hostname(self, mew_hostname: str) -> Hostname:
        return self.appliance.set_hostname(mew_hostname)
