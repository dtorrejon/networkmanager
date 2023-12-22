from unittest.mock import Mock
from tenant.application.usecases.users.read_user import ReadUser


def test_read_user_with_existing_username():
    mock_user_repository = Mock()
    mock_user_repository.get_user.return_value = {"username": "existing_user"}
    read_user = ReadUser(mock_user_repository)
    assert read_user.read_user("existing_user") == {"username": "existing_user"}


def test_read_user_with_nonexistent_username():
    mock_user_repository = Mock()
    mock_user_repository.get_user.return_value = None
    read_user = ReadUser(mock_user_repository)
    assert read_user.read_user("nonexistent_user") is None


def test_read_user_by_mail_with_existing_email():
    mock_user_repository = Mock()
    mock_user_repository.get_user_by_mail.return_value = {"email": "existing_email@example.com"}
    read_user = ReadUser(mock_user_repository)
    assert read_user.read_user_by_mail("existing_email@example.com") == {"email": "existing_email@example.com"}


def test_read_user_by_mail_with_nonexistent_email():
    mock_user_repository = Mock()
    mock_user_repository.get_user_by_mail.return_value = None
    read_user = ReadUser(mock_user_repository)
    assert read_user.read_user_by_mail("nonexistent_email@example.com") is None
