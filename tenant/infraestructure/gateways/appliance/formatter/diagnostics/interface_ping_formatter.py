from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.diagnostics.ping import Ping


class IPingFormatter(metaclass=ABCMeta):

    @abstractmethod
    def format(self, source: str, destination: str, response: str) -> Ping:
        ...
