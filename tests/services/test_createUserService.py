import pytest

from ...app.services.user.createUserService import CreateUserService
from ...app.libs.exceptions import ArgumentException


def test_emailless_call_raises_exception():
    with pytest.raises(ArgumentException):
        service = CreateUserService(user_repository=None, user_factory=None)
        service.call({'name': 'andreu', 'password': 'password123'})


def test_nameless_call_raises_exception():
    with pytest.raises(ArgumentException):
        service = CreateUserService(user_repository=None, user_factory=None)
        service.call({'email': 'aramos@buitre.com', 'password': 'password123'})


def test_passwordless_call_raises_exception():
    with pytest.raises(ArgumentException):
        service = CreateUserService(user_repository=None, user_factory=None)
        service.call({'email': 'aramos@buitre.com', 'name': 'andreu'})

