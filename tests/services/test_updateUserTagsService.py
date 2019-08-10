import pytest

from ...app.entities.tag import Tag
from ...app.utils.exceptions import ArgumentException
from ...app.services.profile.updateUserTagsService import UpdateUserTagsService


class FakeTagRepository:
    @staticmethod
    def get_by_name(tag_name):
        if tag_name == "Bicicletas":
            return Tag("Bicicletas")

    @staticmethod
    def remove_from_user(user_id):
        pass

    @staticmethod
    def add_to_user(user_id, tag):
        pass

    @staticmethod
    def get_by_user_id(user_id):
        if user_id == 1:
            return [Tag("Bicicletas")]


@pytest.fixture
def service():
    service = UpdateUserTagsService(
        tag_repository=FakeTagRepository
    )
    return service


def test_no_arguments(service):
    with pytest.raises(ArgumentException):
        service.call({})


def test_no_tags_argument(service):
    with pytest.raises(ArgumentException):
        service.call({'user_id': 1})


def test_emtpy_tags_argument(service):
    with pytest.raises(ArgumentException):
        service.call({'user_id': 1, 'tags': []})


def test_tag_added(service):
    tags = ["Bicicletas"]
    user_tags = service.call({'user_id': 1, 'tags': tags})
    assert len(user_tags) == 1

