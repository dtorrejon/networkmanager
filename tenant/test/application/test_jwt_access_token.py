import pytest
from jose import JWTError

from tenant.application.jwt_access_token import JWTAccessToken


def test_generate_token():
    user = "test_user"
    token_info = JWTAccessToken.generate_token(user)
    assert "access_token" in token_info
    assert "token_type" in token_info
    assert token_info["token_type"] == JWTAccessToken.TOKEN_TYPE
    decoded_token = JWTAccessToken.decode_token(token_info["access_token"])
    assert decoded_token["username"] == user


def test_decode_token():
    with pytest.raises(JWTError):
        JWTAccessToken.decode_token("invalid_token")
