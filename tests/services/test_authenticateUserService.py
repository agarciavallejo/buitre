import pytest

from ...app.utils.exceptions import ArgumentException, InvalidTokenException, ExpiredTokenException
from ...app.services.user.authenticateUserService import AuthenticateUserService


def dummy_verify_token(token):
    if token == "invalid_token":
        raise InvalidTokenException
    if token == "expired_token":
        raise ExpiredTokenException
    return 123


@pytest.fixture
def service():
    service = AuthenticateUserService(
        token_verifier=dummy_verify_token
    )
    return service


def test_tokenless_call(service):
    with pytest.raises(ArgumentException):
        service.call({})


def test_invalid_token(service):
    with pytest.raises(InvalidTokenException):
        service.call({'token': 'invalid_token'})


def test_expired_token(service):
    with pytest.raises(ExpiredTokenException):
        service.call({'token': 'expired_token'})


def test_valid_token(service):
    user_id = service.call({'token': 'valid_token'})
    assert user_id == 123
