import pytest
from ...app.services.user.createUserService import CreateUserService
from ...app.utils.exceptions import ArgumentException, EmailInUseException


def test_emailless_call_raises_exception():
    with pytest.raises(ArgumentException):
        service = CreateUserService(user_repository=None, user_factory=None, password_hasher=None)
        service.call({'name': 'andreu', 'password': 'password123'})


def test_nameless_call_raises_exception():
    with pytest.raises(ArgumentException):
        service = CreateUserService(user_repository=None, user_factory=None, password_hasher=None)
        service.call({'email': 'aramos@buitre.com', 'password': 'password123'})


def test_passwordless_call_raises_exception():
    with pytest.raises(ArgumentException):
        service = CreateUserService(user_repository=None, user_factory=None, password_hasher=None)
        service.call({'email': 'aramos@buitre.com', 'name': 'andreu'})


def test_already_existing_email_check():
    with pytest.raises(EmailInUseException):
        class FakeRepo:
            @staticmethod
            def get_by_email(email):
                return "not None value"

        service = CreateUserService(user_repository=FakeRepo, user_factory=None, password_hasher=None)
        service.call({'email': 'aramos@buitre.com', 'password': 'pwd123', 'name': 'Andreu'})


def test_password_is_hashed():
    class fakeRepo:
        @staticmethod
        def get_by_email(email):
            return None
        @staticmethod
        def persist(user):
            return user
    class fakeFactory:
        @staticmethod
        def create(name,email,password):
            return {'name':name, 'email':email, 'password':password}
    def dummyHash(password):
        return 'hashed'+password

    service = CreateUserService(
        user_repository=fakeRepo,
        user_factory=fakeFactory,
        password_hasher=dummyHash
    )
    result = service.call({'name': "Andreu", 'email': "aramos@buitre.com", 'password': "pass123"})

    assert result['password'] == 'hashedpass123'

