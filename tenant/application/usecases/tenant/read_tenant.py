from tenant.domain.ports.tenant.interface_read_tenant import IReadTenant
from tenant.domain.schemas.tenants.tenant import Tenant
from tenant.infraestructure.gateways.interface_tenant_repository import ITenantRepository


class ReadTenant(IReadTenant):

    def __init__(self, tenant_repository: ITenantRepository):
        self.tenant_repository = tenant_repository

    def read_tenant(self) -> Tenant:
        return self.tenant_repository.get_tenant()




