from pydantic import BaseModel
from tenant.domain.schemas.users.user import User


class Users(BaseModel):
    users: list[User]

    class Config:
        json_schema_extra = {
            "example": {
                "users": [
                    {
                        "username": "user1",
                        "email": "user1@mymail.com",
                        "name": "user",
                        "surname": "one",
                        "role": "admin"
                    },
                    {
                        "username": "user2",
                        "email": "user2@mymail.com",
                        "name": "user",
                        "surname": "two",
                        "role": "editor"
                    },
                    {
                        "username": "user3",
                        "email": "user3@mymail.com",
                        "name": "user",
                        "surname": "three",
                        "role": "viewer"
                    }
                ]
            }
        }
