import pytest

from ...app.entities.user import User
from ...app.services.profile.updateProfileService import UpdateProfileService

from ...app.utils.exceptions import ArgumentException


class FakeUserRepo:
    @staticmethod
    def get_by_id(user_id):
        if user_id == 1:
            user = User("Andreu", "aramos@buitre.com", "123")
            user.id = 1
            return user

    @staticmethod
    def persist(user):
        return user


@pytest.fixture()
def service():
    service = UpdateProfileService(
        user_repository=FakeUserRepo
    )
    return service


def test_arguments(service):
    with pytest.raises(ArgumentException):
        service.call({})


def test_update_name(service):
    user = service.call({'user_id': 1, 'name': "Andreu Ramos"})
    assert user['name'] == "Andreu Ramos"


def test_update_location(service):
    user = service.call({'user_id': 1, 'latitude': 39.6196049, 'longitude': 2.6004091})
    assert user['latitude'] == 39.6196049
    assert user['longitude'] == 2.6004091


def test_update_radius(service):
    user = service.call({'user_id': 1, 'radius': 5000})
    assert user['radius'] == 5000


def test_update_picture(service):
    user = service.call({'user_id': 1, 'profile_picture': "http://cdn.buitre.com/profile-00001.png"})
    assert user['profile_picture'] == "http://cdn.buitre.com/profile-00001.png"

