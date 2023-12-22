from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tenant.domain.models.repository_type import RepositoryType
from tenant.application.usecases.users.check_user_credentials import CheckUserCredentials
from tenant.application.usecases.users.read_user import ReadUser
from tenant.application.hasher import Hasher
from tenant.application.jwt_access_token import JWTAccessToken
from tenant.application.usecases.users.update_user import UpdateUser
from tenant.domain.schemas.tokens.token_response import TokenResponse
from tenant.domain.schemas.users.existing_user import ExistingUser
from tenant.domain.schemas.users.own_user import OwnUser
from tenant.domain.schemas.users.user import User
from tenant.domain.ports.haser_interface import IHasher
from tenant.domain.ports.users.interface_update_user import IUpdateUser
from tenant.infraestructure.adapters.repositories.factories.user_repository_factory import UserRepositoryFactory
from tenant.infraestructure.gateways.interface_user_repository import IUserRepository

PREFIX: str = "/api/v1/authentication"

auth_router = APIRouter(prefix=PREFIX, responses={404: {"message": "NOT FOUND"}},
                        tags=["User Authentication"])
oauth2 = OAuth2PasswordBearer(tokenUrl=f"{PREFIX}/login", auto_error=True)

REPOSITORY: RepositoryType = RepositoryType.mongo_db_user
repo: IUserRepository = UserRepositoryFactory.get_repository(REPOSITORY)

hasher: IHasher = Hasher()


async def auth_user(token: str = Depends(oauth2)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "bearer"})

    try:
        username: str = JWTAccessToken.decode_token(token).get("username")
        if username is None or username == "":
            raise credentials_exception

    except Exception:
        raise credentials_exception

    return username


async def current_user(username: str = Depends(auth_user)) -> dict:
    user = ReadUser(repo)
    return user.read_user(username)


@auth_router.post("/login", status_code=200, response_model=TokenResponse)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_auth = CheckUserCredentials(repo, hasher)
    if user_auth.check_credentials(username=form.username, password=form.password):
        return JWTAccessToken.generate_token(form.username)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Credentials. Access not granted",
                            headers={"WWW-Authenticate": "Bearer"})


@auth_router.get("/me", response_model=User)
async def me(user: User = Depends(current_user)):
    return user


@auth_router.patch("/modify", status_code=201, response_model=User)
async def modify(user_to_update: OwnUser, user: User = Depends(current_user)) -> dict:
    user_dict: dict = user_to_update.model_dump()
    user_dict["username"] = user.get("username")

    try:
        user_to_update_in_db: ExistingUser = ExistingUser(**user_dict)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ERROR: Wrong user input data")

    user: IUpdateUser = UpdateUser(repo)
    return user.update_user(user_to_update_in_db)
