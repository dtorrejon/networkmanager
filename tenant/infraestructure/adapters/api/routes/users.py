from fastapi import APIRouter, HTTPException, Depends
from pydantic import EmailStr
from starlette import status
from tenant.domain.models.repository_type import RepositoryType
from tenant.domain.models.role_checker import RoleChecker
from tenant.application.usecases.users.create_user import CreateUser
from tenant.application.usecases.users.delete_user import DeleteUser
from tenant.application.usecases.users.read_all_users import ReadAllUsers
from tenant.application.usecases.users.read_user import ReadUser
from tenant.application.usecases.users.update_user import UpdateUser
from tenant.domain.models.role import Role
from tenant.domain.schemas.users.updating_user import UpdatingUser
from tenant.domain.schemas.users.users import Users
from tenant.domain.schemas.users.delete_user_response import DeleteUserResponse
from tenant.domain.schemas.users.new_user import NewUser
from tenant.domain.schemas.users.user import User
from tenant.infraestructure.adapters.repositories.factories.user_repository_factory import UserRepositoryFactory

users_router = APIRouter(prefix="/api/v1/users", tags=["Organization Users"])

REPOSITORY: RepositoryType = RepositoryType.mongo_db_user
repo = UserRepositoryFactory.get_repository(RepositoryType.mongo_db_user)

allow_access = RoleChecker([Role.admin])


@users_router.get("/", response_model=Users, dependencies=[Depends(allow_access)])
async def read_all_users() -> dict:
    return ReadAllUsers(repo).read_all_users()


@users_router.get("/{username}", response_model=User, dependencies=[Depends(allow_access)])
async def read_user(username: str) -> dict:
    if not await user_exist(username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ERROR: User NOT found", )
    return ReadUser(repo).read_user(username)


@users_router.post("/", status_code=201, response_model=User, dependencies=[Depends(allow_access)])
async def create_user(new_user: NewUser) -> dict:
    if await user_exist(new_user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ERROR: User exists")

    if await email_exist(new_user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ERROR: email is being used")

    return CreateUser(repo).create_user(new_user)


@users_router.patch("/", status_code=201, response_model=User, dependencies=[Depends(allow_access)])
async def update_user(existing_user: UpdatingUser):
    if not await user_exist(existing_user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ERROR: User NOT found, can't be updated")

    return UpdateUser(repo).update_user(existing_user)


@users_router.delete("/{username}", status_code=202, response_model=DeleteUserResponse,
                     dependencies=[Depends(allow_access)])
async def delete_user(username: str) -> dict:
    if not await user_exist(username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ERROR: User NOT found, can't be deleted")

    return DeleteUser(repo).delete_user(username)


async def user_exist(username: str) -> bool:
    response: dict = ReadUser(repo).read_user(username)
    if response != {}:
        return True

    return False


async def email_exist(email: EmailStr) -> bool:

    response: dict = ReadUser(repo).read_user_by_mail(email)
    if response != {}:
        return True
    return False
