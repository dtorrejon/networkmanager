from abc import abstractmethod, ABCMeta

from tenant.domain.schemas.node.node import Node
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance


class IApplianceFactory(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_appliance(node: Node) -> Appliance:
        ...
