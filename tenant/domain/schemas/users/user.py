from pydantic import BaseModel, EmailStr

from tenant.domain.models.role import Role


class User(BaseModel):
    username: str
    email: EmailStr
    name: str | None = ""
    surname: str | None = ""
    role: Role

    class Config:
        json_schema_extra = {
            "example": {
                "username": "user1",
                "email": "user1@mymail.com",
                "name": "user",
                "surname": "one",
                "role": "editor"
            }
        }
