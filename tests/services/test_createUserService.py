import pytest
from pytest_mock import mocker

from ...app.services.user.createUserService import CreateUserService
from ...app.entities.user import User, UserRepository
from ...app.libs.exceptions import ArgumentException, EmailInUseException


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
    # CUTRE, s'ha de fer amb cualque mock per verificar que sa funcio get_by_email se crida amb so valor que toca
    with pytest.raises(EmailInUseException):
        class FakeRepo:
            @staticmethod
            def get_by_email(email):
                return "not None value"

        service = CreateUserService(user_repository=FakeRepo, user_factory=None, password_hasher=None)
        service.call({'email': 'aramos@buitre.com', 'password': 'pwd123', 'name': 'Andreu'})

