import pytest
from ...app.utils.exceptions import ArgumentException, AuthenticationException
from ...app.services.user.loginUserService import LoginUserService
from ...app.entities.user import User


class fakeRepo:
    @staticmethod
    def get_by_email(email):
        if email == "unexisting@buitre.com":
            return None
        user = User('test', 'test@test.com', 'test123')
        user.password = 'hashed_password'
        user.is_valid = True
        return user

    @staticmethod
    def persist(user):
        return user


def password_hasher_func(hashed_password, password):
    if password == "wrong":
        return False
    return True


class fakeTokenManager:
    @staticmethod
    def generate_session_token(anything):
        return "this-is-a-token"


@pytest.fixture(scope="module")
def service():
    service = LoginUserService(fakeRepo, fakeTokenManager.generate_session_token, password_hasher_func)
    return service


# TEST CASES
def test_email_required(service):
    with pytest.raises(ArgumentException):
        service.call({'password': "123"})


def test_password_required(service):
    with pytest.raises(ArgumentException):
        service.call({'email': "andreu@buitre.com"})


def test_unexisting_user(service):
    with pytest.raises(AuthenticationException):
        service.call({'email': "unexisting@buitre.com", 'password': "123"})


def test_wrong_password(service):
    with pytest.raises(AuthenticationException):
        service.call({'email': "andre@buitre.com", 'password': "wrong"})


def test_login_token(service):
    token = service.call({'email': "andre@buitre.com", 'password': "unhashed_password"})
    assert token == 'this-is-a-token'
