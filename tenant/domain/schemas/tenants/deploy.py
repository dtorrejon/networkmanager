from pydantic import BaseModel

from tenant.domain.schemas.users.new_user import NewUser


class Deploy(BaseModel):
    name: str
    address: str | None = ""
    phone: str | None = ""
    user: NewUser


    class Config:
        json_schema_extra = {
            "example": {
                "name": "Company Name",
                "address": "John Doe Str. 122",
                "phone": "+1 123 456 78",
                "user": {
                    "name": "john",
                    "role": "admin",
                    "email": "john@mail.me",
                    "username": "john",
                    "password": "1234",
                    "surname": "surname",
                },
            }
        }