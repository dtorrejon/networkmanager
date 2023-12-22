from abc import ABCMeta, abstractmethod

from tenant.domain.schemas.tenants.tenant import Tenant


class IReadTenant(metaclass=ABCMeta):

    @abstractmethod
    def read_tenant(self) -> Tenant:
        ...
