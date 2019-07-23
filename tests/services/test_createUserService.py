import pytest
import mock
from ...app.services.user.createUserService import CreateUserService
from ...app.utils.exceptions import ArgumentException, EmailInUseException


def test_emailless_call_raises_exception():
    with pytest.raises(ArgumentException):
        service = CreateUserService(
            user_repository=None,
            user_factory=None,
            password_hasher=None,
            validation_token_generator=None,
            email_factory=None,
            email_sender=None
        )
        service.call({'name': 'andreu', 'password': 'password123'})


def test_nameless_call_raises_exception():
    with pytest.raises(ArgumentException):
        service = CreateUserService(
            user_repository=None,
            user_factory=None,
            password_hasher=None,
            validation_token_generator=None,
            email_factory=None,
            email_sender=None
        )
        service.call({'email': 'aramos@buitre.com', 'password': 'password123'})


def test_passwordless_call_raises_exception():
    with pytest.raises(ArgumentException):
        service = CreateUserService(
            user_repository=None,
            user_factory=None,
            password_hasher=None,
            validation_token_generator=None,
            email_factory=None,
            email_sender=None
        )
        service.call({'email': 'aramos@buitre.com', 'name': 'andreu'})


def test_already_existing_email_check():
    with pytest.raises(EmailInUseException):
        class FakeRepo:
            @staticmethod
            def get_by_email(email):
                return "not None value"

        service = CreateUserService(
            user_repository=FakeRepo,
            user_factory=None,
            password_hasher=None,
            validation_token_generator=None,
            email_factory=None,
            email_sender=None
        )
        service.call({'email': 'aramos@buitre.com', 'password': 'pwd123', 'name': 'Andreu'})


def test_password_is_hashed():
    class fakeRepo:
        first_time = True
        @staticmethod
        def get_by_email(email):
            if fakeRepo.first_time:
                fakeRepo.first_time = False
                return None
            return

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

    service = CreateUserService(
        user_repository=fakeRepo,
        user_factory=fakeFactory,
        password_hasher=dummyHash,
        validation_token_generator=generateDummyToken,
        email_factory=fakeEmailFactory,
        email_sender=fakeEmailSender
    )
    result = service.call({'name': "Andreu", 'email': "aramos@buitre.com", 'password': "pass123"})
    print(result)
    assert result.password == 'hashedpass123'
