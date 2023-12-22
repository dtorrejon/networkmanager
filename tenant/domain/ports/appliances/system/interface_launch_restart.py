
from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.system.restart import Restart


class ILaunchRestart(metaclass=ABCMeta):

    @abstractmethod
    def restart(self) -> Restart:
        ...