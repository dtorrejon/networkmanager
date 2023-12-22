import binascii

from cryptography.fernet import Fernet
import hashlib


class PasswordCrypt:

    def __init__(self):
        SECRET_KEY = b'03NtEhWQufnTe_lllCGJFlMdcbSwejEP0Aq6ASzhzBs='
        self.cipher = Fernet(SECRET_KEY)

    def encode_password(self, password: str):
        return self.cipher.encrypt(password.encode()).decode()

    def decode_password(self, encrypted_password: str) -> str:
        return self.cipher.decrypt(encrypted_password).decode()

    @staticmethod
    def generate_secret_key() -> str:
        return Fernet.generate_key().decode()
