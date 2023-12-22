from tenant.domain.ports.tenant.interface_create_tenant import ICreateTenant
from tenant.domain.schemas.tenants import tenant
from tenant.domain.schemas.tenants.deploy import Deploy
from tenant.domain.schemas.tenants.new_tenant import NewTenant
from tenant.infraestructure.gateways.factories.interface_create_tenant_repository import ICreateTenantRepository


class CreateTenant(ICreateTenant):

    def __init__(self, create_tenant_repository: ICreateTenantRepository):
        self.create_tenant_repository: ICreateTenantRepository = create_tenant_repository

    def create(self, tenant: NewTenant) -> dict:
        repo_response = self.create_tenant_repository.create_tenant(tenant)
        return {
            "database_response": repo_response
        }

