import pytest
from ...app.libs.exceptions import ArgumentException, AuthenticationException
from ...app.services.user.loginUserService import LoginUserService
from ...app.entities.user import User


def test_email_required():
    with pytest.raises(ArgumentException):
        service = LoginUserService(None, None, None)
        service.call({'password': "123"})


def test_password_required():
    with pytest.raises(ArgumentException):
        service = LoginUserService(None, None, None)
        service.call({'email': "andreu@buitre.com"})


def test_unexisting_user():
    with pytest.raises(AuthenticationException):
        class fakeRepo:
            @staticmethod
            def get_by_email(email):
                return None

        service = LoginUserService(fakeRepo, None, None)
        service.call({'email': "andreu@buitre.com", 'password': "123"})


def test_wrong_password():
    with pytest.raises(AuthenticationException):
        class fakeRepo:
            @staticmethod
            def get_by_email(email):
                user = User
                user.password = 'hashed_password'
                return user

        def password_hasher_func(hashed_password, password):
            return False

        service = LoginUserService(fakeRepo, None, password_hasher_func)
        service.call({'email': "andre@buitre.com", 'password': "unhashed_password"})


def test_login_token():
    class fakeRepo:
        @staticmethod
        def get_by_email(email):
            user = User('test', 'test@test.com', 'test123')
            user.password = 'hashed_password'
            user.is_valid = True
            return user
        @staticmethod
        def persist(user):
            return user

    def password_hasher_func(hashed_password, password):
        return True

    class fakeTokenManager:
        @staticmethod
        def generate_login_token(anything):
            return "this-is-a-token"

    service = LoginUserService(fakeRepo, fakeTokenManager, password_hasher_func)
    token = service.call({'email': "andre@buitre.com", 'password': "unhashed_password"})
    assert token == 'this-is-a-token'
