from jose import jwt, JWTError
from tenant.domain.ports.interface_access_token import IAccessToken
from datetime import datetime, timedelta


class JWTAccessToken(IAccessToken):
    TOKEN_DURATION: int = 60*24*7
    ALGORITHM: str = "HS256"
    TOKEN_TYPE: str = "bearer"
    SECRET_KEY: str = "1ad7a653da7a5efbba59dac7c88c2d0deb2e9152288e98189489dec1bfbab523"

    @classmethod
    def generate_token(cls, user: str) -> dict:

        access_token: dict = {"sub": user, "exp": datetime.utcnow() + timedelta(minutes=cls.TOKEN_DURATION)}

        return {"access_token": jwt.encode(access_token, cls.SECRET_KEY, algorithm=cls.ALGORITHM),
                "token_type": cls.TOKEN_TYPE}

    @classmethod
    def decode_token(cls, token: str) -> dict:
        try:
            username = jwt.decode(token, cls.SECRET_KEY, algorithms=cls.ALGORITHM).get("sub")
            return {"username": username}

        except JWTError as error:
            raise error

