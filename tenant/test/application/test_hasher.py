from tenant.application.hasher import Hasher


def test_compare_hash():
    hasher = Hasher()
    plain_password = "password123"
    hashed_password = hasher.generate_hash(plain_password)
    assert hasher.compare_hash(plain_password, hashed_password) is True
    hashed_password = hasher.generate_hash(plain_password)
    assert hasher.compare_hash("wrongpassword", hashed_password) is False


def test_generate_hash():
    hasher = Hasher()
    plain_password = "password123"
    hashed_password1 = hasher.generate_hash(plain_password)
    hashed_password2 = hasher.generate_hash(plain_password)
    assert hashed_password1 != hashed_password2
