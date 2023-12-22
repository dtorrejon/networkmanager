from pydantic import BaseModel, EmailStr


class OwnUser(BaseModel):
    email: EmailStr | None = ""
    password: str | None = ""
    name: str | None = ""
    surname: str | None = ""


    class Config:
        json_schema_extra = {
            "example": {
                "email": "user1@mymail.com",
                "password": "pass",
                "name": "user",
                "surname": "one"
            }
        }
