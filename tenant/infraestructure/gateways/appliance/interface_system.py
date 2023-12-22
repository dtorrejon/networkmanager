from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.system.hostname import Hostname
from tenant.domain.schemas.appliances.system.restart import Restart


class ISystem(metaclass=ABCMeta):

    @abstractmethod
    def restart(self) -> Restart:
        ...

    @abstractmethod
    def set_hostname(self, new_hostname: str) -> Hostname:
        ...