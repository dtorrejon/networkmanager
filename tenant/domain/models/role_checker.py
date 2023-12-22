
from fastapi import Depends, HTTPException

from tenant.domain.models.role import Role
from tenant.domain.schemas.users.user import User
from tenant.infraestructure.adapters.api.routes.authentication import current_user


class RoleChecker:
    def __init__(self, allowed_roles: list[Role]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(current_user)):
        if user.get("role") not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")