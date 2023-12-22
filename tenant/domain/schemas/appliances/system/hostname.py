from pydantic import BaseModel


class Hostname(BaseModel):
    status: str
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok",
                "message": "New hostname switch01, successfully updated"
            }
        }
