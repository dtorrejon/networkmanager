from pydantic import BaseModel


class ExistingTenant(BaseModel):
    address: str | None = ""
    phone: str | None = ""

    class Config:
        json_schema_extra = {
            "example": {
                "address": "John Doe Str. 122",
                "phone": "+1 123 456 78",
            }
        }
