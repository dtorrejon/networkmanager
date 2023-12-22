from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.system.hostname import Hostname


class ISetHostname(metaclass=ABCMeta):

    @abstractmethod
    def set_hostname(self, mew_hostname: str) -> Hostname:
        ...
