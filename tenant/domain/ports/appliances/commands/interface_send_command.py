from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.commands.command import Command


class ISendCommand(metaclass=ABCMeta):

    @abstractmethod
    def send_command(self, command: str) -> Command:
        ...