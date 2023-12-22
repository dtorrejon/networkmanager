from tenant.domain.schemas.appliances.system.hostname import Hostname
from tenant.domain.schemas.appliances.system.restart import Restart
from tenant.infraestructure.gateways.appliance.interface_system import ISystem


class NotImplementedSystem(ISystem):
    def restart(self) -> Restart:
        pass

    def set_hostname(self, new_hostname: str) -> Hostname:
        pass
