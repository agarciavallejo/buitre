import pytest

from ...app.entities.user import User
from ...app.services.user.sendUserRecoveryService import SendUserRecoveryService
from ...app.utils.exceptions import ArgumentException, AuthenticationException


def test_email_required():
    with pytest.raises(ArgumentException):
        service = SendUserRecoveryService(
            user_repository=None,
            email_factory=None,
            email_sender=None,
            token_generator=None
        )
        service.call({})


def test_unexisting_user():
    with pytest.raises(AuthenticationException):
        class fakerepo:
            @staticmethod
            def get_by_email(email):
                return None

        service = SendUserRecoveryService(
            user_repository=fakerepo,
            email_factory=None,
            email_sender=None,
            token_generator=None
        )
        service.call({'email': "email_that_does_not_exist"})


def test_existing_user():
    class fakeRepo:
        @staticmethod
        def get_by_email(email):
            user = User('andreu', 'andreu@andreu.com', '123')
            return user

    class fakeFactory:
        @staticmethod
        def create_recovery_email(name, email, token):
            return "Something"

    class fakeSender:
        @staticmethod
        def send(email):
            return True

    def fakeTokenGenerator(email):
        return "recovery-token"

    service = SendUserRecoveryService(
        user_repository=fakeRepo,
        email_factory=fakeFactory,
        email_sender=fakeSender,
        token_generator=fakeTokenGenerator
    )
    service.call({
        'email': "andreu@andreu.com"
    })
