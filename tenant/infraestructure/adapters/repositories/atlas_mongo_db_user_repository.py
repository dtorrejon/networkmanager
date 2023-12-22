import yaml
import certifi
from pydantic import EmailStr
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient

from tenant.domain.models.file_path import FilePath
from tenant.domain.schemas.users.updating_user import UpdatingUser
from tenant.domain.schemas.users.new_user import NewUser
from tenant.domain.schemas.users.user import User
from tenant.infraestructure.gateways.interface_user_repository import IUserRepository


class AtlasMongoDBUserRepository(IUserRepository):

    def connect(self):
        with open(f"{FilePath.get_path(__file__)}/../../../config_files/config_db.yaml", "r") as file:
            config_file = yaml.safe_load(file)

        self.client: MongoClient = MongoClient(config_file["db_connection"]["url"], tlsCAFile=certifi.where())
        self.db: Database = self.client[str(config_file["db_connection"]["database"])]
        self.collection: Collection = self.db["users"]

    def __init__(self):
        self.collection = None
        self.db = None
        self.client = None
        self.connect()

    def create_user(self, user: NewUser) -> dict:
        self.collection.insert_one(user.model_dump())
        return self.get_user(user.username)

    def get_user(self, username: str) -> dict:
        response: dict = self.collection.find_one({"username": username},
                                                  {"_id": 0, "username": 1, "email": 1, "name": 1, "surname": 1,
                                                   "role": 1})
        if response is not None:
            return response
        else:
            return {}

    def get_all_users(self) -> dict:
        users_response: list[User] = []
        for user in self.collection.find({}, {"_id": 0, "username": 1, "email": 1, "name": 1, "surname": 1, "role": 1}):
            users_response.append(user)
        return {"users": users_response}

    def update_user(self, user: UpdatingUser) -> dict:
        fields_to_update: dict = {}
        for k, v in user.model_dump().items():
            if v != "":
                fields_to_update[k] = v

        self.collection.find_one_and_update({"username": user.username}, {'$set': fields_to_update})
        return self.get_user(user.username)

    def delete_user(self, username: str) -> dict:
        self.collection.delete_one({"username": username})
        if self.get_user(username) == {}:
            return {"message": f"User {username} deleted successfully"}
        else:
            return {"message": f"User {username} couldn't be deleted"}

    def read_password(self, username) -> bool:
        return self.collection.find_one({"username": username},
                                        {"_id": 0, "password": 1})

    def get_user_by_mail(self, email: EmailStr) -> dict:
        response: dict = self.collection.find_one({"email": email},
                                                  {"_id": 0, "username": 1, "email": 1, "name": 1, "surname": 1,
                                                   "role": 1})
        if response is not None:
            return response
        else:
            return {}
