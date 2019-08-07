import pytest

from ...app.entities.comment import Comment
from ...app.entities.opportunity import Opportunity
from ...app.entities.picture import Picture
from ...app.entities.tag import Tag
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
        user.profile_picture = "http://cdn.buitre.com/profile-00001.png"
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

    @staticmethod
    def get_by_liked_by(user_id):
        favorited = []
        if user_id == 1:
            return favorited
        oppo = Opportunity("Oportunidad 3", 2)
        favorited.append(oppo)
        return favorited


class FakeTagRepo:
    @staticmethod
    def get_by_user_id(user_id):
        tags = []
        if user_id == 1:
            return tags
        tag = Tag("Bicicletas")
        tag.id = 1
        tags.append(tag)
        return tags


class FakePictureRepo:
    @staticmethod
    def get_by_opportunity_id(opportunity_id):
        pictures = []
        if opportunity_id != 1:
            return pictures
        picture = Picture(opportunity_id, "http://cdn.buitre.com/opo1-front.png")
        pictures.append(picture)
        return pictures


@pytest.fixture()
def service():
    service = GetProfileService(
        user_repository=FakeUserRepo,
        comment_repository=FakeCommentRepo,
        opportunity_repository=FakeOppoRepo,
        tag_repository=FakeTagRepo,
        picture_repository=FakePictureRepo
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
    assert profile['picture'] == "http://cdn.buitre.com/profile-00001.png"


def test_no_comments(service):
    profile = service.call({'user_id': 1})
    assert len(profile['contributions']) is 0


def test_some_comments(service):
    profile = service.call({'user_id': 2})
    assert len(profile['contributions']) is not 0
    assert profile['contributions'][0]['text'] == "comment text"
    assert profile['contributions'][0]['created_at'] == "2019-08-08 20:18:33"
    assert profile['contributions'][0]['opportunity_id'] == 1
    assert profile['contributions'][0]['opportunity_name'] == "Oportunidad 1"


def test_no_opportunities(service):
    profile = service.call({'user_id': 1})
    assert len(profile['opportunities']) is 0


def test_some_opportunities(service):
    profile = service.call({'user_id': 2})
    assert len(profile['opportunities']) is not 0
    assert profile['opportunities'][0]['name'] == "Oportunidad 2"
    assert profile['opportunities'][0]['id'] == 1
    assert profile['opportunities'][0]['picture'] == "http://cdn.buitre.com/opo1-front.png"


def test_no_tags(service):
    profile = service.call({'user_id': 1})
    assert len(profile['tags']) is 0


def test_some_tags(service):
    profile = service.call({'user_id': 2})
    assert len(profile['tags']) is not 0
    assert profile['tags'][0]['name'] == "Bicicletas"
    assert profile['tags'][0]['id'] == 1


def test_no_favorites(service):
    profile = service.call({'user_id': 1})
    assert len(profile['favorited_opportunities']) is 0


def test_some_favorites(service):
    profile = service.call({'user_id': 2})
    assert len(profile['favorited_opportunities']) is not 0
