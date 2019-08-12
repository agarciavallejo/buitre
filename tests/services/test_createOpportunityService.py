import pytest

from ...app.entities.opportunity import Opportunity
from ...app.entities.picture import Picture
from ...app.services.opportunity.createOpportunityService import CreateOpportunityService
from ...app.utils.exceptions import ArgumentException


class FakeOpportunityFactory:
    @staticmethod
    def create(user_id, name, description, address, latitude, longitude, closing_date):
        oppo = Opportunity(
            name=name,
            user_id=user_id,
            description=description,
            address=address,
            latitude=latitude,
            longitude=longitude,
            closing_date=closing_date,
        )
        return oppo


class FakeOpportunityRepository:
    @staticmethod
    def persist(opportunity):
        return opportunity


class FakePictureFactory:
    @staticmethod
    def create_for_opportunity(opportunity_id, path, user_id):
        return Picture(opportunity_id, path, user_id)


class FakePictureRepository:
    @staticmethod
    def persist(picture):
        return picture


@pytest.fixture()
def service():
    return CreateOpportunityService(
        opportunity_factory=FakeOpportunityFactory,
        opportunity_repository=FakeOpportunityRepository,
        picture_factory=FakePictureFactory,
        picture_repository=FakePictureRepository
    )


def test_arguments_user_id(service):
    with pytest.raises(ArgumentException):
        service.call({
            'name': "Test Oppo",
            'pictures': ['some-path-to-a-picture'],
            'latitude': 39,
            'longitude': 2,
            'address': "fake st. 123",
        })


def test_arguments_name(service):
    with pytest.raises(ArgumentException):
        service.call({
            'user_id': 1,
            'pictures': ['some-path-to-a-picture'],
            'latitude': 39,
            'longitude': 2,
            'address': "fake st. 123",
        })


def test_arguments_pictures(service):
    with pytest.raises(ArgumentException):
        service.call({
            'user_id': 1,
            'name': "Testing Oppo",
            'latitude': 39,
            'longitude': 2,
            'address': "fake st. 123",
        })


def test_arguments_pictures_empty(service):
    with pytest.raises(ArgumentException):
        service.call({
            'user_id': 1,
            'name': "Testing Oppo",
            'pictures': [],
            'latitude': 39,
            'longitude': 2,
            'address': "fake st. 123",
        })


def test_arguments_latitude(service):
    with pytest.raises(ArgumentException):
        service.call({
            'user_id': 1,
            'name': "Test Oppo",
            'pictures': ['some-path-to-a-picture'],
            'longitude': 2,
            'address': "fake st. 123",
        })


def test_arguments_longitude(service):
    with pytest.raises(ArgumentException):
        service.call({
            'user_id': 1,
            'name': "Test Oppo",
            'pictures': ['some-path-to-a-picture'],
            'latitude': 39,
            'address': "fake st. 123",
        })


def test_opportunity_is_returned(service):
    oppo = service.call({
        'user_id': 1,
        'name': "Testing Oppo",
        'pictures': ['https://cdn.buitre.com/opomain_picture.png'],
        'latitude': 39,
        'longitude': 2,
        'address': "fake st. 123",
    })
    assert oppo.name == "Testing Oppo"
    assert oppo.user_id == 1
    assert oppo.latitude == 39
    assert oppo.longitude == 2
    assert oppo.address == "fake st. 123"
