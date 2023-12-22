from pydantic import BaseModel


class Tenant(BaseModel):
    name: str
    address: str | None = ""
    phone: str | None = ""

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Company Name",
                "address": "John Doe Str. 122",
                "phone": "+1 123 456 78",
            }
        }
