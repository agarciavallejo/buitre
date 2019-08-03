import pytest

from ...app.entities.user import User
from ...app.services.user.getUserService import GetUserService
from ...app.utils.exceptions import ArgumentException, UserNotFoundException


class fakeRepo():
    @staticmethod
    def get_by_id(user_id):
        if user_id == 999:
            return None
        user = User('andreu', 'andreu@buitre.com', '123')
        return user


@pytest.fixture()
def service():
    service = GetUserService(
        user_repository=fakeRepo
    )
    return service


def test_call_without_argument(service):
    with pytest.raises(ArgumentException):
        service.call({})


def test_user_does_not_exist(service):
    with pytest.raises(UserNotFoundException):
        service.call({'user_id': 999})


def test_user_data(service):
    user = service.call({'user_id': 1})
    assert isinstance(user, dict)
    assert user['name'] == 'andreu'
    assert user['email'] == 'andreu@buitre.com'
