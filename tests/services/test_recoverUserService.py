import pytest

from ...app.entities.user import User
from ...app.utils.exceptions import ArgumentException, InvalidTokenException, ExpiredTokenException
from ...app.services.user.recoverUserService import RecoverUserService


def test_arguments_token():
    with pytest.raises(ArgumentException):
        service = RecoverUserService(
            token_verifier=None,
            user_repository=None,
            password_hasher=None
        )
        service.call({})


def test_arguments_password():
    with pytest.raises(ArgumentException):
        service = RecoverUserService(
            token_verifier=None,
            user_repository=None,
            password_hasher=None
        )
        service.call({'recovery_token': "a-token"})


def test_expired_token():
    with pytest.raises(ExpiredTokenException):
        def fakeVerifier(token):
            raise ExpiredTokenException

        service = RecoverUserService(
            token_verifier=fakeVerifier,
            user_repository=None,
            password_hasher=None
        )
        service.call({'recovery_token': "expired", 'password': "123"})


def test_invalid_token():
    with pytest.raises(InvalidTokenException):
        def fakeVerifier(token):
            raise InvalidTokenException

        service = RecoverUserService(
            token_verifier=fakeVerifier,
            user_repository=None,
            password_hasher=None
        )
        service.call({'recovery_token': "invalid", 'password': "123"})


def test_unexisting_user():
    with pytest.raises(InvalidTokenException):
        class fakeRepo:
            @staticmethod
            def get_by_email(email):
                return None

        def fakeVerifier(token):
            return "some@email.com"

        service = RecoverUserService(
            token_verifier=fakeVerifier,
            user_repository=fakeRepo,
            password_hasher=None
        )
        service.call({'recovery_token': "token", 'password': "123"})

def test_new_password_is_hashed():
    class fakeRepo:
        @staticmethod
        def get_by_email(email):
            return User('andreu', 'andreu@buitre.com', 'old_hashed_pwd')
        @staticmethod
        def persist(user):
            return user

    def fakeVerifier(token):
        return "some@email.com"

    def fakeHasher(password):
        return "hashed_password"

    service = RecoverUserService(
        token_verifier=fakeVerifier,
        user_repository=fakeRepo,
        password_hasher=fakeHasher
    )
    user = service.call({'recovery_token': "token", 'password': "123"})
    assert user.password == "hashed_password"