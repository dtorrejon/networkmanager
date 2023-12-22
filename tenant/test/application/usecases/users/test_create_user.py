from unittest.mock import Mock
from tenant.application.usecases.users.create_user import CreateUser
from tenant.domain.schemas.users.new_user import NewUser


def test_create_user_with_valid_data():
    mock_user_repository = Mock()
    mock_user_repository.create_user.return_value = {"username": "new_user", "password": "hashed_password123"}
    create_user = CreateUser(mock_user_repository)
    new_user = NewUser(username="new_user", password="password123", email="mail@gmail.com", first_name="John",  last_name="Doe", phone_number="1234567890", role="admin")
    assert create_user.create_user(new_user) == {"username": "new_user", "password": "hashed_password123"}


def test_create_user_with_existing_username():
    mock_user_repository = Mock()
    mock_user_repository.create_user.side_effect = Exception("User already exists")
    create_user = CreateUser(mock_user_repository)
    new_user = NewUser(username="existing_user", password="password123", email="nomail@mail.com", first_name="John", last_name="Doe", phone_number="1234567890", role="admin")
    try:
        create_user.create_user(new_user)
    except Exception as e:
        assert str(e) == "User already exists"


def test_create_user_with_empty_username():
    mock_user_repository = Mock()
    create_user = CreateUser(mock_user_repository)
    new_user = NewUser(username="", password="password123", email="nomail@mail.com", first_name="John", last_name="Doe", phone_number="1234567890", role="admin")
    try:
        create_user.create_user(new_user)
    except Exception as e:
        assert str(e) == "Username cannot be empty"
