import certifi
import yaml
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from tenant.domain.models.file_path import FilePath
from tenant.domain.schemas.node.deleted_node_response import DeletedNodeResponse
from tenant.domain.schemas.node.existing_node import ExistingNode
from tenant.domain.schemas.node.node import Node
from tenant.domain.schemas.node.node_response import NodeResponse
from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials
from tenant.infraestructure.gateways.interface_node_repository import INodeRepository


class AtlasMongoDBNodeRepository(INodeRepository):

    def connect(self):
        with open(f"{FilePath.get_path(__file__)}/../../../config_files/config_db.yaml", "r") as file:
            config_file = yaml.safe_load(file)

        self.client: MongoClient = MongoClient(config_file["db_connection"]["url"], tlsCAFile=certifi.where())
        self.db: Database = self.client[str(config_file["db_connection"]["database"])]
        self.collection: Collection = self.db["nodes"]

    def __init__(self):
        self.collection = None
        self.db = None
        self.client = None
        self.connect()

    def save(self, node: Node) -> NodeResponse:
        data = node.model_dump()
        data["ipAddress"] = str(node.model_dump()["ipAddress"])

        self.collection.insert_one(data)
        return self.retrieve(node.name)

    def retrieve(self, node_name: str) -> NodeResponse:
        response: dict = self.collection.find_one({"name": node_name},
                                                  {"_id": 0, "name": 1, "vendor": 1, "technology": 1, "model": 1,
                                                   "softwareVersion": 1,
                                                   "ipAddress": 1, "protocol": 1, "port": 1})
        if response is not None:
            return NodeResponse(**response)
        else:
            return {}

    def retrieve_with_credentials(self, node_name: str) -> NodeWithCredentials:
        response: dict = self.collection.find_one({"name": node_name},
                                                  {"_id": 0, "name": 1, "vendor": 1, "technology": 1, "model": 1,
                                                   "softwareVersion": 1,
                                                   "ipAddress": 1, "protocol": 1, "port": 1, "username": 1,
                                                   "password": 1})
        if response is not None:
            return NodeWithCredentials(**response)
        else:
            return {}

    def retrieve_all(self) -> list[NodeResponse]:
        nodes_response: list[NodeResponse] = []
        for node in self.collection.find({}, {"_id": 0, "name": 1, "vendor": 1, "technology": 1, "model": 1,
                                              "softwareVersion": 1,
                                              "ipAddress": 1, "protocol": 1, "port": 1}):
            nodes_response.append(node)

        return nodes_response

    def update(self, node: ExistingNode) -> NodeResponse:
        fields_to_update: dict = {}
        for k, v in node.model_dump().items():
            if v != "":
                if k == "newName":
                    fields_to_update["name"] = v
                if k == "port" and v == -1:
                    ...
                else:
                    fields_to_update[k] = v

        self.collection.find_one_and_update({"name": node.name}, {'$set': fields_to_update})
        if fields_to_update["name"]:
            return self.retrieve(fields_to_update["name"])

        return self.retrieve(node.name)

    def delete(self, node_name: str) -> DeletedNodeResponse:
        self.collection.delete_one({"name": node_name})
        if self.retrieve(node_name) == {}:
            return DeletedNodeResponse(status=f"ok", message=f"Node {node_name} has been deleted")
        else:
            return DeletedNodeResponse(status=f"nok", message=f"Node {node_name} couldn't be deleted")
