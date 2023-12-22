from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "user1"
            }
        }
