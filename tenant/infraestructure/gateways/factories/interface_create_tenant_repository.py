from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.tenants.new_tenant import NewTenant


class ICreateTenantRepository(metaclass=ABCMeta):

    @abstractmethod
    def create_tenant(self, tenant: NewTenant) -> dict:
        ...
