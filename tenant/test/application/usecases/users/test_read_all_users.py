from unittest.mock import Mock
from tenant.application.usecases.users.read_all_users import ReadAllUsers


def test_read_all_users_with_users_present():
    mock_user_repository = Mock()
    mock_user_repository.get_all_users.return_value = [{"username": "user1"}, {"username": "user2"}]
    read_all_users = ReadAllUsers(mock_user_repository)
    assert read_all_users.read_all_users() == [{"username": "user1"}, {"username": "user2"}]


def test_read_all_users_with_no_users_present():
    mock_user_repository = Mock()
    mock_user_repository.get_all_users.return_value = []
    read_all_users = ReadAllUsers(mock_user_repository)
    assert read_all_users.read_all_users() == []

