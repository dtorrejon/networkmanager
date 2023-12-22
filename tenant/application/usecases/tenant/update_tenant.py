
from tenant.domain.ports.tenant.interface_update_tenant import IUpdateTenant
from tenant.domain.schemas.tenants.tenant import Tenant
from tenant.domain.schemas.tenants.existing_tenant import ExistingTenant
from tenant.infraestructure.gateways.interface_tenant_repository import ITenantRepository


class UpdateTenant(IUpdateTenant):
    def __init__(self, tenant_repository: ITenantRepository):
        self.tenant_repository = tenant_repository

    def update_tenant(self, tenant: ExistingTenant) -> Tenant:
        return self.tenant_repository.update_tenant(tenant)
