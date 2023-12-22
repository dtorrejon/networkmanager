import certifi
import yaml
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient

from tenant.domain.models.file_path import FilePath
from tenant.domain.schemas.tenants.tenant import Tenant
from tenant.domain.schemas.tenants.existing_tenant import ExistingTenant
from tenant.infraestructure.gateways.interface_tenant_repository import ITenantRepository


class AtlasMongoDBTenantRepository(ITenantRepository):
    def connect(self):
        with open(f"{FilePath.get_path(__file__)}/../../../config_files/config_db.yaml", "r") as file:
            config_file = yaml.safe_load(file)
        self.client = MongoClient(config_file["db_connection"]["url"], tlsCAFile=certifi.where())
        self.db: Database = self.client[str(config_file["db_connection"]["database"])]
        self.collection: Collection = self.db["tenant"]

    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.connect()

    def get_tenant(self) -> Tenant:
        response: dict = self.collection.find_one({}, {"_id": 0, "name": 1, "phone": 1, "address": 1})
        if response is not None:
            tenant = Tenant(**response)
            return tenant
        else:
            return {}

    def update_tenant(self, tenant: ExistingTenant) -> Tenant:
        fields_to_update: dict = {}
        for k, v in tenant.model_dump().items():
            if v != "":
                fields_to_update[k] = v

        if self.collection.find_one_and_update({}, {'$set': fields_to_update}) is None:
            return {}

        return self.get_tenant()
