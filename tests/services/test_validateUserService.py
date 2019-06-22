import pytest
from ...app.libs.exceptions import ArgumentException, UserValidationException
from ...app.services.user.ValidateUserService import ValidateUserService
from ...app.entities.user import User


def test_missing_user_id():
    with pytest.raises(ArgumentException):
        service = ValidateUserService(
            user_repository=None
        )

        service.call({})


def test_unexisting_user():
    with pytest.raises(UserValidationException):
        class fakeRepo:
            @staticmethod
            def get_by_id(id):
                None
        service = ValidateUserService(
            user_repository=fakeRepo
        )

        service.call({'id': 1})


def test_user_is_validated():
    class fakeRepo:
        @staticmethod
        def get_by_id(id):
            return "Not none"
        @staticmethod
        def validate(id):
            user = User("andreu", "aramos@buitre.com", "123")
            user.id = id
            user.is_valid = True
            return user

    service = ValidateUserService(
        user_repository=fakeRepo
    )
    user = service.call({'id': 1})

    assert user.is_valid
