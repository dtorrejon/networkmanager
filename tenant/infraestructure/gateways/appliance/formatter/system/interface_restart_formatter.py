from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.system.restart import Restart


class IRestartFormatter(metaclass=ABCMeta):

    @abstractmethod
    def format(self, restart_text: str) -> Restart:
        ...
