from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.tenants.tenant import Tenant
from tenant.domain.schemas.tenants.existing_tenant import ExistingTenant


class ITenantRepository(metaclass=ABCMeta):

    @abstractmethod
    def get_tenant(self) -> Tenant:
        ...

    @abstractmethod
    def update_tenant(self, tenant: ExistingTenant) -> Tenant:
        ...
