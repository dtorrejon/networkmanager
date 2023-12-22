from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.diagnostics.arp import Arp


class ILaunchArp(metaclass=ABCMeta):

    @abstractmethod
    def arp(self) -> list[Arp]:
        ...
