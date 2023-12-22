from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from tenant.application.usecases.tenant.create_tenant import CreateTenant
from tenant.domain.models import repository_type
from tenant.domain.models.repository_type import RepositoryType
from tenant.application.usecases.tenant.read_tenant import ReadTenant
from tenant.application.usecases.tenant.update_tenant import UpdateTenant
from tenant.domain.models.role import Role
from tenant.domain.ports.tenant.interface_update_tenant import IUpdateTenant
from tenant.domain.ports.tenant.interface_read_tenant import IReadTenant
from tenant.domain.models.role_checker import RoleChecker
from tenant.domain.schemas.tenants import tenant
from tenant.domain.schemas.tenants.deploy import Deploy
from tenant.domain.schemas.tenants.new_tenant import NewTenant
from tenant.domain.schemas.tenants.tenant import Tenant
from tenant.domain.schemas.tenants.existing_tenant import ExistingTenant
from tenant.infraestructure.adapters.repositories.atlas_mongo_db_tenant_repository import ITenantRepository
from tenant.infraestructure.adapters.repositories.factories.atlas_mongo_db_create_tenant_repository_factory import \
    CreateTenantRepositoryFactory
from tenant.infraestructure.adapters.repositories.factories.tenant_repository_factory import TenantRepositoryFactory

tenant_router = APIRouter(prefix="/api/v1/organization", tags=["Organization info"])

allow_access_read_tenant = RoleChecker([Role.admin, Role.editor, Role.viewer])
allow_access_update_tenant = RoleChecker([Role.admin])

repo: ITenantRepository = TenantRepositoryFactory.get_repository(RepositoryType.mongo_db_tenant)


@tenant_router.get("/", status_code=200, response_model=Tenant, dependencies=[Depends(allow_access_read_tenant)])
async def read_tenant() -> Tenant:
    return ReadTenant(repo).read_tenant()


@tenant_router.patch("/", status_code=201, response_model=ExistingTenant,
                     dependencies=[Depends(allow_access_update_tenant)])
async def update_tenant(tenant: ExistingTenant):
    response: Tenant = UpdateTenant(repo).update_tenant(tenant)

    if response == {}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ERROR: please, check request")

    return response

@tenant_router.post("/", status_code=201)
async def deploy(tenant_signup: NewTenant) -> dict:
    create_tenant = CreateTenant(CreateTenantRepositoryFactory.get_repository(RepositoryType.mongo_db_create_tenant))
    create_tenant.create(tenant_signup)
    return {"message": f"{tenant_signup.name} organization and {tenant_signup.user.username} user, successfully created"}
