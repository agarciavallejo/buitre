import pytest
from ...app.utils.exceptions import ArgumentException, \
    UserValidationException, InvalidTokenException, ExpiredTokenException
from ...app.services.user.validateUserService import ValidateUserService
from ...app.entities.user import User


def test_missing_user_id():
    with pytest.raises(ArgumentException):
        service = ValidateUserService(
            user_repository=None,
            validation_token_verifier=None
        )

        service.call({})


def test_invalid_token():
    with pytest.raises(UserValidationException):
        def dummyverifier(token):
            raise InvalidTokenException()

        service = ValidateUserService(
            validation_token_verifier=dummyverifier,
            user_repository=None
        )

        service.call({'validation_token': "invalid_token"})


def test_expired_token():
    with pytest.raises(UserValidationException):
        def dummyverifier(token):
            raise ExpiredTokenException()

        service = ValidateUserService(
            validation_token_verifier=dummyverifier,
            user_repository=None
        )

        service.call({'validation_token': "expired_token"})


def test_unexisting_user():
    with pytest.raises(UserValidationException):
        class fakeRepo:
            @staticmethod
            def get_by_email(email):
                None

        def dummyverifier(token):
            return "email@email.com"

        service = ValidateUserService(
            user_repository=fakeRepo,
            validation_token_verifier=dummyverifier
        )

        service.call({'validation_token': "something"})


def test_user_is_validated():
    class fakeRepo:
        @staticmethod
        def get_by_email(email):
            user = User("andreu", email, "123")
            user.id = id
            user.is_valid = False
            return user

        @staticmethod
        def persist(user):
            return user

    def dummy_verifier(token):
        return True

    service = ValidateUserService(
        user_repository=fakeRepo,
        validation_token_verifier=dummy_verifier
    )
    user = service.call({'validation_token': "sometoken"})

    assert user.is_valid
