import datetime
import json

import certifi
import yaml
from pymongo.mongo_client import MongoClient

from tenant.application.hasher import Hasher
from tenant.domain.models.file_path import FilePath
from tenant.domain.models.repository_type import RepositoryType
from tenant.domain.schemas.tenants.new_tenant import NewTenant
from tenant.infraestructure.gateways.factories.interface_create_tenant_repository import ICreateTenantRepository


class CreateAtlasMongoDBTenantRepository(ICreateTenantRepository):
    REPOSITORY: RepositoryType = RepositoryType.mongo_db_user

    def __init__(self):
        with open(f"{FilePath.get_path(__file__)}/../../../config_files/config_db.yaml", "r") as file:
            config_file = yaml.safe_load(file)
        self.client = MongoClient(config_file["db_connection"]["url"], tlsCAFile=certifi.where())
        self.db = ""
        self.collection = ""

    def create_tenant(self, new_tenant: NewTenant) -> dict:
        with open(f"{FilePath.get_path(__file__)}/../../../config_files/config_db.yaml", "r") as file:
            config_file = yaml.safe_load(file)
            self.db = self.client[new_tenant.name]

        with open(f"{FilePath.get_path(__file__)}/../../../config_files/config_db.yaml", "w") as file:
            config_file["db_connection"]["database"] = new_tenant.name
            yaml.safe_dump(config_file, file)

        if new_tenant.name not in self.client.list_database_names():
            self.collection = self.db["tenant"]
            self.collection.insert_one(
                {"name": new_tenant.name, "address": new_tenant.address, "phone": new_tenant.phone})

            client = self.client
            db = client["tenantsDB"]
            collection = db["tenants"]
            tenant_dict = self.collection.find_one({"name": new_tenant.name}, {"_id": 1, "name": 1,
                                                                               "address": 1, "phone": 1})

            tenant_dict.update({"created_at": datetime.datetime.now(tz=datetime.timezone.utc)})
            collection.insert_one(tenant_dict)

            response: dict = self.collection.find_one({"name": new_tenant.name}, {"_id": 0, "name": 1,
                                                                                  "address": 1, "phone": 1})

            self.collection = self.db["users"]
            new_tenant.user.role = "admin"
            new_tenant.user.password = str(Hasher.generate_hash(new_tenant.user.password))
            self.collection.insert_one(new_tenant.user.model_dump())
            response = self.collection.find_one({"username": new_tenant.user.name},
                                                {"_id": 0, "username": 1, "email": 1, "name": 1, "surname": 1,
                                                 "role": 1})
            self.collection = self.db["compatible_nodes"]

            with open(f"{FilePath.get_path(__file__)}/../../../config_files/compatible_nodes.json", "r") as file:
                self.collection.insert_many(json.load(file))

            self.collection = self.db["tenant"]

            return response
        else:
            return {}
