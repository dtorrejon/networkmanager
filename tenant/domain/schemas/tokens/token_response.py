from pydantic import BaseModel

from tenant.domain.models.role import Role


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "Bearer",
                "token_type": "jklhfkjasdkjf978643kj.-vd++dfpokoipprjelfidnsjkshgkfsdjklñfhldashliv"
            }
        }
