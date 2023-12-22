from unittest.mock import Mock
from tenant.application.usecases.users.delete_user import DeleteUser


def test_delete_user_with_existing_username():
    mock_user_repository = Mock()
    mock_user_repository.delete_user.return_value = {"username": "existing_user", "status": "deleted"}
    delete_user = DeleteUser(mock_user_repository)
    assert delete_user.delete_user("existing_user") == {"username": "existing_user", "status": "deleted"}


def test_delete_user_with_no_existing_username():
    mock_user_repository = Mock()
    mock_user_repository.delete_user.side_effect = Exception("User does not exist")
    delete_user = DeleteUser(mock_user_repository)
    try:
        delete_user.delete_user("nonexistent_user")
    except Exception as e:
        assert str(e) == "User does not exist"
