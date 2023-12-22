from pydantic import BaseModel


class Command(BaseModel):
    command: str
    response: str

    class Config:
        json_schema_extra = {
            "example": {
                "command": "show vlan brief",
                "response": f"\nVLAN Name                             Status    Ports\n---- ----------------------------"
                            f"---- --------- -------------------------------\n"
                            f"1    default                          active    Et0/0, Et0/1, Et0/3, Et1/0, Et1/1, Et1/3\n"
                            f"99   VLAN0099                         active    \n789  VLAN0789                         "
                            f"active    Et3/1\n1002 fddi-default                     act/unsup \n1003 token-ring-default"
                            f"               act/unsup \n1004 fddinet-default                  act/unsup \n"
                            f"1005 trnet-default                    act/unsup "
            }
        }
