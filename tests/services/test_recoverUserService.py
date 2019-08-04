import pytest

from ...app.entities.user import User
from ...app.utils.exceptions import ArgumentException, InvalidTokenException, ExpiredTokenException
from ...app.services.user.recoverUserService import RecoverUserService


class FakeRepo:
    @staticmethod
    def get_by_email(email):
        if email == "unexisting@email.com":
            return None
        return User('andreu', 'andreu@buitre.com', 'old_hashed_pwd')

    @staticmethod
    def persist(user):
        return user


def fake_verifier(token):
    if token == "unexisting_user_token":
        return "unexisting@email.com"
    if token == "invalid":
        raise InvalidTokenException
    if token == "expired":
        raise ExpiredTokenException
    return "some@email.com"


def fake_hasher(password):
    return "hashed_password"


@pytest.fixture()
def service():
    service = RecoverUserService(
        token_verifier=fake_verifier,
        user_repository=FakeRepo,
        password_hasher=fake_hasher
    )
    return service


def test_arguments_token(service):
    with pytest.raises(ArgumentException):
        service.call({})


def test_arguments_password(service):
    with pytest.raises(ArgumentException):
        service.call({'recovery_token': "a-token"})


def test_expired_token(service):
    with pytest.raises(ExpiredTokenException):
        service.call({'recovery_token': "expired", 'password': "123"})


def test_invalid_token(service):
    with pytest.raises(InvalidTokenException):
        service.call({'recovery_token': "invalid", 'password': "123"})


def test_unexisting_user(service):
    with pytest.raises(InvalidTokenException):
        service.call({'recovery_token': "unexisting_user_token", 'password': "123"})


def test_new_password_is_hashed(service):
    user = service.call({'recovery_token': "token", 'password': "123"})
    assert user.password == "hashed_password"
