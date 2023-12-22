from pydantic import BaseModel

from tenant.domain.models.status import Status


class DeletedNodeResponse(BaseModel):
    status: Status
    message: str
