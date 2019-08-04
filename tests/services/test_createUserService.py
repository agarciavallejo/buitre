import pytest
import mock
from ...app.services.user.createUserService import CreateUserService
from ...app.utils.exceptions import ArgumentException, EmailInUseException


class fakeRepo:
    @staticmethod
    def get_by_email(email):
        if email == "existing@buitre.com":
            return "not None value"
        return None

    @staticmethod
    def persist(user):
        return user


class fakeFactory:
    @staticmethod
    def create(name, email, password):
        dummyuser = mock.Mock()
        dummyuser.name = name
        dummyuser.email = email
        dummyuser.password = password
        dummyuser.validation_token = None
        return dummyuser


class fakeEmailFactory:
    @staticmethod
    def create_user_validation_email(name, email, validation_token):
        return object()


class fakeEmailSender:
    @staticmethod
    def send(email):
        pass


def dummyHash(password):
    return 'hashed' + password


def generateDummyToken(email):
    return "dummytoken"


@pytest.fixture(scope="module")
def service():
    service = CreateUserService(
        user_repository=fakeRepo,
        user_factory=fakeFactory,
        password_hasher=dummyHash,
        validation_token_generator=generateDummyToken,
        email_factory=fakeEmailFactory,
        email_sender=fakeEmailSender
    )
    return service


# TEST CASES
def test_emailless_call_raises_exception(service):
    with pytest.raises(ArgumentException):
        service.call({'name': 'andreu', 'password': 'password123'})


def test_nameless_call_raises_exception(service):
    with pytest.raises(ArgumentException):
        service.call({'email': 'aramos@buitre.com', 'password': 'password123'})


def test_passwordless_call_raises_exception(service):
    with pytest.raises(ArgumentException):
        service.call({'email': 'aramos@buitre.com', 'name': 'andreu'})


def test_already_existing_email_check(service):
    with pytest.raises(EmailInUseException):
        service.call({'email': 'existing@buitre.com', 'password': 'pwd123', 'name': 'Andreu'})


def test_password_is_hashed(service):
    result = service.call({'name': "Andreu", 'email': "aramos@buitre.com", 'password': "pass123"})
    assert result.password == 'hashedpass123'
