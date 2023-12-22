from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.appliances.commands.command import Command
from tenant.domain.schemas.appliances.commands.script import Script


class ISendScript(metaclass=ABCMeta):

    @abstractmethod
    def send_script(self, script: Script) -> list[Command]:
        ...
