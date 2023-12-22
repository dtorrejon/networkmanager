from unittest.mock import Mock
from tenant.application.usecases.tenant.read_tenant import ReadTenant


def test_read_tenant_with_existing_tenant():
    mock_tenant_repository = Mock()
    mock_tenant_repository.get_tenant.return_value = {"name": "existing_tenant"}
    read_tenant = ReadTenant(mock_tenant_repository)
    assert read_tenant.read_tenant() == {"name": "existing_tenant"}


def test_read_tenant_with_no_tenant():
    mock_tenant_repository = Mock()
    mock_tenant_repository.get_tenant.return_value = None
    read_tenant = ReadTenant(mock_tenant_repository)
    assert read_tenant.read_tenant() is None
