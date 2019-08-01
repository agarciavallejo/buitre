import pytest
from ...app.utils.exceptions import ArgumentException, \
    UserValidationException, InvalidTokenException, ExpiredTokenException
from ...app.services.user.validateUserService import ValidateUserService
from ...app.entities.user import User


class fakeRepo:
    @staticmethod
    def get_by_email(email):
        if email != "email@email.com":
            return None
        user = User("andreu", email, "123")
        user.id = id
        user.is_valid = False
        return user

    @staticmethod
    def persist(user):
        return user


def dummy_verifier(token):
    if token == "invalid_token":
        raise InvalidTokenException
    if token == "expired_token":
        raise ExpiredTokenException
    if token == "unexisting_user":
        return False
    return "email@email.com"


@pytest.fixture(scope="module")
def service():
    service = ValidateUserService(
        user_repository=fakeRepo,
        validation_token_verifier=dummy_verifier
    )
    return service


# TEST CASES
def test_missing_user_id(service):
    with pytest.raises(ArgumentException):
        service.call({})


def test_invalid_token(service):
    with pytest.raises(UserValidationException):
        service.call({'validation_token': "invalid_token"})


def test_expired_token(service):
    with pytest.raises(UserValidationException):
        service.call({'validation_token': "expired_token"})


def test_unexisting_user(service):
    with pytest.raises(UserValidationException):
        service.call({'validation_token': "unexisting_user"})


def test_user_is_validated(service):
    user = service.call({'validation_token': "sometoken"})
    assert user.is_valid
