from unittest.mock import Mock
from tenant.application.usecases.users.check_user_credentials import CheckUserCredentials


def test_check_credentials_with_correct_password():
    mock_user_repository = Mock()
    mock_user_repository.read_password.return_value = {"password": "hashed_password123"}
    mock_hasher = Mock()
    mock_hasher.compare_hash.return_value = True
    check_user_credentials = CheckUserCredentials(mock_user_repository, mock_hasher)
    assert check_user_credentials.check_credentials("username", "password123") is True


def test_check_credentials_with_incorrect_password():
    mock_user_repository = Mock()
    mock_user_repository.read_password.return_value = {"password": "hashed_password123"}
    mock_hasher = Mock()
    mock_hasher.compare_hash.return_value = False
    check_user_credentials = CheckUserCredentials(mock_user_repository, mock_hasher)
    assert check_user_credentials.check_credentials("username", "wrongpassword") is False


def test_check_credentials_with_nonexistent_user():
    mock_user_repository = Mock()
    mock_user_repository.read_password.return_value = None
    mock_hasher = Mock()
    check_user_credentials = CheckUserCredentials(mock_user_repository, mock_hasher)
    assert check_user_credentials.check_credentials("nonexistent_user", "password123") is False
