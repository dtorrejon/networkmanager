from enum import Enum


class VlanMode(str, Enum):
    ACCESS = "access"
    TRUNK = "trunk"
    NATIVE = "native"
