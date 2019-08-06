import pytest

from ...app.entities.opportunity import Opportunity
from ...app.entities.comment import Comment
from ...app.entities.user import User
from ...app.utils.exceptions import ArgumentException, UserNotFoundException
from ...app.services.profile.getProfileService import GetProfileService


class FakeUserRepo:
    @staticmethod
    def get_by_id(id):
        if id == 999:
            return None
        user = User("Andreu", "aramos@buitre.com", "123")
        user.score = 500
        user.radius = 1000
        user.latitude = 39.6196049
        user.longitude = 2.6004091
        return user


class FakeCommentRepo:
    @staticmethod
    def get_by_user_id(user_id):
        comments = list()
        if user_id == 1:
            return comments
        comment = Comment("comment text", user_id, 1)
        comment.created_at = "2019-08-08 20:18:33"
        comments.append(comment)
        return comments


class FakeOppoRepo:
    @staticmethod
    def get_by_id(id):
        if id == 1:
            return Opportunity("Oportunidad 1", 23)

    @staticmethod
    def get_by_user_id(user_id):
        opportunities = []
        if user_id == 1:
            return opportunities
        oppo = Opportunity("Oportunidad 2", 2)
        oppo.id = 1
        opportunities.append(oppo)
        return opportunities


@pytest.fixture()
def service():
    service = GetProfileService(
        user_repository=FakeUserRepo,
        comment_repository=FakeCommentRepo,
        opportunity_repository=FakeOppoRepo
    )
    return service


def test_argument(service):
    with pytest.raises(ArgumentException):
        service.call({})


def test_not_found_user(service):
    with pytest.raises(UserNotFoundException):
        service.call({'user_id': 999})


def test_user_data(service):
    profile = service.call({'user_id': 1})
    assert profile['name'] == "Andreu"
    assert profile['email'] == "aramos@buitre.com"
    assert profile['score'] == 500
    assert profile['longitude'] == 2.6004091
    assert profile['latitude'] == 39.6196049
    assert profile['radius'] == 1000


def test_no_comments(service):
    profile = service.call({'user_id': 1})
    assert profile['contributions'] == []


def test_some_comments(service):
    profile = service.call({'user_id': 2})
    assert profile['contributions'][0] is not None
    assert profile['contributions'][0]['text'] == "comment text"
    assert profile['contributions'][0]['created_at'] == "2019-08-08 20:18:33"
    assert profile['contributions'][0]['opportunity_id'] == 1
    assert profile['contributions'][0]['opportunity_name'] == "Oportunidad 1"


def test_no_opportunities(service):
    profile = service.call({'user_id': 1})
    assert profile['opportunities'] == []
