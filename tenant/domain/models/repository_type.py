from enum import Enum


class RepositoryType(str, Enum):
    mongo_db_tenant = "mongo_db_tenant"
    mongo_db_user = "mongo_db_user"
    mongo_db_create_tenant = "mongo_db_create_tenant"
    mock_tenant = "mock_tenant"
    mock_user = "mock_user"
