from abc import ABCMeta, abstractmethod
from typing import Any, Optional, Union
from tenant.application.usecases.node.read_node_with_credentials import ReadNodeWithCredentials
from tenant.domain.schemas.appliances.commands.command import Command
from tenant.domain.schemas.appliances.commands.script import Script
from tenant.domain.schemas.appliances.diagnostics.arp import Arp
from tenant.domain.schemas.appliances.diagnostics.ping import Ping
from tenant.domain.schemas.appliances.diagnostics.ping_command_fields import PingCommandFields
from tenant.domain.schemas.appliances.diagnostics.route import Route
from tenant.domain.schemas.appliances.diagnostics.trace_route import TraceRoute
from tenant.domain.schemas.appliances.diagnostics.trace_route_command_fields import TraceRouteCommandFields
from tenant.domain.schemas.appliances.network_interfaces.network_interface import NetworkInterface
from tenant.domain.schemas.appliances.network_interfaces.network_interface_brief import NetworkInterfaceBrief
from tenant.domain.schemas.appliances.system.hostname import Hostname
from tenant.domain.ports.nodes.interface_read_node_with_credentials import IReadNodeWithCredentials
from tenant.domain.models.repository_type import RepositoryType
from tenant.domain.schemas.appliances.system.restart import Restart
from tenant.domain.schemas.appliances.vlans.vlan_brief import VlanBrief
from tenant.domain.schemas.appliances.vlans.vlan_resume import VlanResume
from tenant.domain.schemas.appliances.vlans.vlan_trunk import VlanTrunk
from tenant.infraestructure.adapters.appliances.not_implemented.not_implemented_network_interfaces import \
    NotImplementedNetworkInterfaces
from tenant.infraestructure.adapters.appliances.not_implemented.not_implemented_node import \
    NotImplementedDiagnostics
from tenant.infraestructure.adapters.appliances.not_implemented.not_implemented_routes import NotImplementedRoutes
from tenant.infraestructure.adapters.appliances.not_implemented.not_implemented_svi import NotImplementedSvi
from tenant.infraestructure.adapters.appliances.not_implemented.not_implemented_system import NotImplementedSystem
from tenant.infraestructure.adapters.appliances.not_implemented.not_implemented_vlan import NotImplementedVlan
from tenant.infraestructure.gateways.appliance.interface_diagnostics import IDiagnostics

from tenant.infraestructure.gateways.appliance.interface_network_interfaces import \
    INetworkInterfaces
from tenant.infraestructure.gateways.appliance.interface_routes import IRoutes
from tenant.infraestructure.gateways.appliance.interface_svi import ISvi
from tenant.infraestructure.gateways.appliance.interface_system import ISystem
from tenant.infraestructure.adapters.repositories.factories.node_respository_factory import NodeRepositoryFactory
from tenant.infraestructure.gateways.appliance.interface_vlan import IVlan


class Appliance(metaclass=ABCMeta):

    def __init__(self, node_name: str):
        repository = NodeRepositoryFactory.get_repository(RepositoryType.mongo_db_user)
        read_node: IReadNodeWithCredentials = ReadNodeWithCredentials(repository)
        self.node = read_node.retrieve(node_name)
        self._diagnostics: IDiagnostics = NotImplementedDiagnostics()
        self._system: ISystem = NotImplementedSystem()
        self._network_interfaces: INetworkInterfaces = NotImplementedNetworkInterfaces()
        self._routes: IRoutes = NotImplementedRoutes()
        self._svi: ISvi = NotImplementedSvi()
        self._vlan: IVlan = NotImplementedVlan()

    @abstractmethod
    def connect(self) -> Any:
        ...

    @abstractmethod
    def send_command(self, command: str) -> Command:
        ...

    @abstractmethod
    def send_script(self, script: Script) -> list[Command]:
        ...

    @abstractmethod
    def service_status(self) -> bool:
        ...

    @property
    def diagnostics(self):
        return self._diagnostics

    @diagnostics.setter
    def diagnostics(self, diagnostics: IDiagnostics):
        self._diagnostics = diagnostics

    def arp(self) -> list[Arp]:
        return self._diagnostics.arp()

    def ping(self, ping_command_fields: PingCommandFields) -> Ping:
        return self._diagnostics.ping(ping_command_fields)

    def trace_route(self, trace_route_command_fields: TraceRouteCommandFields) -> TraceRoute:
        return self._diagnostics.traceroute(trace_route_command_fields)


    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, system: ISystem):
        self._system = system

    def restart(self) -> Restart:
        return self._system.restart()

    def set_hostname(self, new_hostname: str) -> Hostname:
        return self._system.set_hostname(new_hostname)

    @property
    def network_interfaces(self):
        return self._network_interfaces

    @network_interfaces.setter
    def network_interfaces(self, network_interfaces: INetworkInterfaces):
        self._network_interfaces = network_interfaces

    def display(self, interface: Optional[str] = None) -> list[NetworkInterface]:
        return self._network_interfaces.display(interface)

    def display_interface_brief(self) -> list[NetworkInterfaceBrief]:
        return self._network_interfaces.display_interface_brief()

    def no_shutdown(self, interface: str) -> NetworkInterface:
        return self._network_interfaces.no_shutdown(interface)

    def shutdown(self, interface: str) -> NetworkInterface:
        return self._network_interfaces.shutdown(interface)

    def set_ip(self, interface: str, ip_address: str) -> NetworkInterface:
        return self._network_interfaces.set_ip(interface, ip_address)

    def set_description(self, interface: str, description: str) -> NetworkInterface:
        return self._network_interfaces.set_description(interface, description)

    @property
    def svi(self):
        return self._svi

    @svi.setter
    def svi(self, svi: ISvi):
        self._svi = svi

    def create_svi(self, vlan_id: str) -> NetworkInterface:
        return self._svi.create_svi(vlan_id)

    def set_svi_ip(self, svi: str, ip_address: str) -> NetworkInterface:
        return self._svi.set_svi_ip(svi, ip_address)

    def delete_svi(self, vlan_id: str) -> list[NetworkInterface]:
        return self._svi.delete_svi(vlan_id)

    @property
    def vlan(self):
        return self._vlan

    @vlan.setter
    def vlan(self, vlan: IVlan):
        self._vlan = vlan

    def display_vlan_brief(self) -> list[VlanBrief]:
        return self._vlan.display_vlan_brief()

    def display_vlan_trunk(self) -> list[VlanTrunk]:
        return self._vlan.display_vlan_trunk()

    def set_vlan_access(self, interface: str, vlan_id: int, encapsulation: str) -> list[VlanBrief]:
        return self._vlan.set_vlan_access(interface, vlan_id, encapsulation)

    def set_vlan_native(self, interface: str, vlan_id: int, encapsulation: str) -> list[VlanTrunk]:
        return self._vlan.set_vlan_native(interface, vlan_id, encapsulation)

    def set_vlan_trunk(self, interface: str, vlan_id: list[int], encapsulation: str) -> list[VlanTrunk]:
        return self._vlan.set_vlan_trunk(interface, vlan_id, encapsulation)

    def remove_vlan(self, interface: str | None, vlan_id: Union[int, str]) -> VlanResume:
        return self._vlan.remove_vlan(interface, vlan_id)

    @property
    def routes(self):
        return self._routes

    @routes.setter
    def routes(self, routes: IRoutes):
        self._routes = routes

    def routing_table(self) -> list[Route]:
        return self._routes.routing_table()

    def set_default_gateway(self, ip: str) -> list[Route]:
        return self._routes.set_default_gateway(ip)

    def set_static_route(self, ip_and_mask_in_cidr: str, ip_next_hop: str) -> list[Route]:
        return self._routes.set_static_route(ip_and_mask_in_cidr, ip_next_hop)
