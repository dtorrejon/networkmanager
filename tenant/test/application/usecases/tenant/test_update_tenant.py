from unittest.mock import Mock
from tenant.application.usecases.tenant.update_tenant import UpdateTenant
from tenant.domain.schemas.tenants.existing_tenant import ExistingTenant


def test_update_tenant_with_existing_tenant():
    mock_tenant_repository = Mock()
    mock_tenant_repository.update_tenant.return_value = {"name": "existing_tenant"}
    update_tenant = UpdateTenant(mock_tenant_repository)
    existing_tenant = ExistingTenant(name="existing_tenant")
    assert update_tenant.update_tenant(existing_tenant) == {"name": "existing_tenant"}


def test_update_tenant_with_nonexistent_tenant():
    mock_tenant_repository = Mock()
    mock_tenant_repository.update_tenant.side_effect = Exception("Tenant does not exist")
    update_tenant = UpdateTenant(mock_tenant_repository)
    nonexistent_tenant = ExistingTenant(name="nonexistent_tenant")
    try:
        update_tenant.update_tenant(nonexistent_tenant)
    except Exception as e:
        assert str(e) == "Tenant does not exist"
