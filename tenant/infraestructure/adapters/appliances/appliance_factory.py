from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.infraestructure.adapters.appliances.cisco.router.cisco_router_ios_ssh import CiscoRouterIosSsh
from tenant.infraestructure.adapters.appliances.cisco.router.cisco_router_ios_telnet import CiscoRouterIosTelnet
from tenant.infraestructure.adapters.appliances.cisco.switchl3.cisco_switchl3_ios_ssh import CiscoSwitchl3IosSsh
from tenant.infraestructure.adapters.appliances.cisco.switchl3.cisco_switchl3_ios_telnet import CiscoSwitchl3IosTelnet
from tenant.infraestructure.adapters.appliances.mikrotik.switchl3.mikrotik_switchl3_api import MikrotikSwitchl3Api
from tenant.infraestructure.gateways.appliance.abstract_appliance import Appliance
from tenant.infraestructure.gateways.factories.interface_appliance_factory import IApplianceFactory


class ApplianceFactory(IApplianceFactory):

    @staticmethod
    def get_appliance(node: NodeWithCredentials) -> Appliance:
        if node.vendor == f"cisco" and node.technology == "switchl3" and node.protocol == "telnet":
            return CiscoSwitchl3IosTelnet(node.name)

        elif node.vendor == f"cisco" and node.technology == "switchl3" and node.protocol == "ssh":
            return CiscoSwitchl3IosSsh(node.name)

        elif node.vendor == f"cisco" and node.technology == "router" and node.protocol == "telnet":
            return CiscoRouterIosTelnet(node.name)

        elif node.vendor == f"cisco" and node.technology == "router" and node.protocol == "ssh":
            return CiscoRouterIosSsh(node.name)

        elif node.vendor == f"mikrotik" and node.technology == "switchl3":
            return MikrotikSwitchl3Api(node.name)

        elif node.vendor == f"mikrotik" and "routeros" in node.softwareVersion.lower():
            return MikrotikSwitchl3Api(node.name)


