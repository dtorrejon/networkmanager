from tenant.domain.schemas.users.user import User


class NewUser(User):
    password: str

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