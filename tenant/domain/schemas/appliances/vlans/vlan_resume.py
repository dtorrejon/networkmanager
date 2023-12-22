from pydantic import BaseModel

from tenant.domain.schemas.appliances.vlans.vlan_brief import VlanBrief
from tenant.domain.schemas.appliances.vlans.vlan_trunk import VlanTrunk


class VlanResume(BaseModel):
    vlanAccess: list[VlanBrief]
    vlanTrunk: list[VlanTrunk]
