from unittest.mock import Mock
from tenant.application.usecases.users.update_user import UpdateUser
from tenant.domain.schemas.users.updating_user import UpdatingUser


def test_update_user_with_existing_username_and_password():
    mock_user_repository = Mock()
    mock_user_repository.update_user.return_value = {"username": "existing_user", "password": "new_hashed_password"}
    update_user = UpdateUser(mock_user_repository)
    updating_user = UpdatingUser(username="existing_user", password="new_password")
    assert update_user.update_user(updating_user) == {"username": "existing_user", "password": "new_hashed_password"}


def test_update_user_with_existing_username_and_no_password():
    mock_user_repository = Mock()
    mock_user_repository.update_user.return_value = {"username": "existing_user", "password": ""}
    update_user = UpdateUser(mock_user_repository)
    updating_user = UpdatingUser(username="existing_user", password="")
    assert update_user.update_user(updating_user) == {"username": "existing_user", "password": ""}


def test_update_user_with_nonexistent_username():
    mock_user_repository = Mock()
    mock_user_repository.update_user.side_effect = Exception("User does not exist")
    update_user = UpdateUser(mock_user_repository)
    updating_user = UpdatingUser(username="nonexistent_user", password="new_password")
    try:
        update_user.update_user(updating_user)
    except Exception as e:
        assert str(e) == "User does not exist"
