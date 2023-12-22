from tenant.application.password_crypt import PasswordCrypt


def test_encode_password():
    password_crypt = PasswordCrypt()
    password = "test_password"
    encoded_password = password_crypt.encode_password(password)
    assert password != encoded_password


def test_decode_password():
    password_crypt = PasswordCrypt()
    password = "test_password"
    encoded_password = password_crypt.encode_password(password)
    decoded_password = password_crypt.decode_password(encoded_password)
    assert password == decoded_password


def test_generate_secret_key():
    password_crypt = PasswordCrypt()
    secret_key = password_crypt.generate_secret_key()
    assert secret_key != ""
    assert isinstance(secret_key, str)
    assert secret_key[-1] == "="


