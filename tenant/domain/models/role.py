from enum import Enum


class Role(str, Enum):
    viewer = "viewer"
    editor = "editor"
    admin = "admin"

