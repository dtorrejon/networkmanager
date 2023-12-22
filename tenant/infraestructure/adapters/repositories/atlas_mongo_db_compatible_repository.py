import certifi
import yaml
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from tenant.domain.models.file_path import FilePath
from tenant.domain.schemas.node.compatible_node_search import CompatibleNodeSearch
from tenant.infraestructure.gateways.interface_compatible_node_repository import ICompatibleNodeRepository


class AtlasMongoDBCompatibleNodeRepository(ICompatibleNodeRepository):

    def connect(self):
        with open(f"{FilePath.get_path(__file__)}/../../../config_files/config_db.yaml", "r") as file:
            config_file = yaml.safe_load(file)

        self.client: MongoClient = MongoClient(config_file["db_connection"]["url"], tlsCAFile=certifi.where())
        self.db: Database = self.client[str(config_file["db_connection"]["database"])]
        self.collection: Collection = self.db["compatible_nodes"]

    def __init__(self):
        self.collection = None
        self.db = None
        self.client = None
        self.connect()

    def retrieve(self, compatible_node: CompatibleNodeSearch) -> list[CompatibleNodeSearch]:

        filtered_query: dict = {key: value for key, value in compatible_node.model_dump().items() if value is not None}
        query_response = self.collection.find(filtered_query, {"_id": 0, "vendor": 1, "model": 1, "technology": 1,
                                                               "softwareVersion": 1})

        response: list[CompatibleNodeSearch] = []
        for document in query_response:
            response.append(document)

        if response is not None:
            return response
        else:
            return {}

    def retrieve_all(self) -> list[CompatibleNodeSearch]:
        nodes_response: list[CompatibleNodeSearch] = []
        for node in self.collection.find({}, {"_id": 0, "vendor": 1, "model": 1, "technology": 1,
                                              "softwareVersion": 1}):
            nodes_response.append(node)

        return nodes_response
