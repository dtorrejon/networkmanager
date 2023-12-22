from pydantic import BaseModel


class Script(BaseModel):
    commands: list[str]

    class Config:
        json_schema_extra = {
            "example": {
                "commands": [
                    "show vlan brief",
                    "sh running-config"
                ]

            }
        }
