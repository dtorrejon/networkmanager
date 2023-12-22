from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.tenants.tenant import Tenant
from tenant.domain.schemas.tenants.existing_tenant import ExistingTenant


class IUpdateTenant(metaclass=ABCMeta):

    @abstractmethod
    def update_tenant(self, tenant: ExistingTenant) -> Tenant:
        ...
