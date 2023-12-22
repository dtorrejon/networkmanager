import requests
import urllib3
from requests.auth import HTTPBasicAuth

from tenant.domain.schemas.node.node_with_credentials import NodeWithCredentials


class MikrotikRouterOSSaveConfig:

    def __init__(self, node: NodeWithCredentials):
        self.node = node
        urllib3.disable_warnings()
        self.__save_config()

    def __save_config(self) -> str:
        url = f"https://{self.node.ipAddress}:{self.node.port}/rest/system/backup/save"
        headers = {"content-type": "application/json"}

        r = requests.request(method="POST", url=url,
                             auth=HTTPBasicAuth(self.node.username, self.node.password),
                             headers=headers,
                             verify=False)

        return "config saved"
