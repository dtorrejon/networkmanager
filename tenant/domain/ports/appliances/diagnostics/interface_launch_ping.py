from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.diagnostics.ping import Ping
from tenant.domain.schemas.appliances.diagnostics.ping_command_fields import PingCommandFields


class ILaunchPing(metaclass=ABCMeta):

    @abstractmethod
    def ping(self, ping_command_fields: PingCommandFields) -> Ping:
        ...