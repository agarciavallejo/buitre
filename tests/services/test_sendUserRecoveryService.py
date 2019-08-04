import pytest

from ...app.entities.user import User
from ...app.services.user.sendUserRecoveryService import SendUserRecoveryService
from ...app.utils.exceptions import ArgumentException, AuthenticationException


class fakeRepo:
    @staticmethod
    def get_by_email(email):
        if email == "email_that_does_not_exist":
            return None
        user = User('andreu', 'andreu@andreu.com', '123')
        return user


class fakeFactory:
    @staticmethod
    def create_user_recovery_email(name, email, token):
        return "Something"


class fakeSender:
    @staticmethod
    def send(email):
        return True


def fakeTokenGenerator(email):
    return "recovery-token"


@pytest.fixture()
def service():
    service = SendUserRecoveryService(
        user_repository=fakeRepo,
        email_factory=fakeFactory,
        email_sender=fakeSender,
        token_generator=fakeTokenGenerator
    )
    return service


def test_email_required(service):
    with pytest.raises(ArgumentException):
        service.call({})


def test_unexisting_user(service):
    with pytest.raises(AuthenticationException):
        service.call({'email': "email_that_does_not_exist"})


def test_existing_user(service):
    service.call({'email': "andreu@andreu.com"})
