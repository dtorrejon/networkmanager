from pydantic import EmailStr

from tenant.domain.models.role import Role
from tenant.domain.schemas.users.user import User


class ExistingUser(User):
    username: str | None = ""
    email: EmailStr | None = ""
    password: str | None = ""
    name: str | None = ""
    surname: str | None = ""
    role: Role | None = ""


    class Config:
        json_schema_extra = {
            "example": {
                "username": "user1",
                "email": "user1@mymail.com",
                "password": "pass",
                "name": "user",
                "surname": "one",
                "role": "editor"
            }
        }