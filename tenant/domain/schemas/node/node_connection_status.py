from enum import Enum


class NodeConnectionStatus(str, Enum):
    ONLINE = "UP"
    OFFLINE = "DOWN"
    ISSUE = "WARNING"
