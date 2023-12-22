from pydantic import BaseModel


class Restart(BaseModel):
    status: str
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "KO",
                "message": "Can't reboot device. Configuration register is 0x0, and must be 0x2102"
            }
        }
