from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.diagnostics.arp import Arp


class IArpFormatter(metaclass=ABCMeta):

    @abstractmethod
    def format(self, arp_text: str) -> Arp:
        ...
