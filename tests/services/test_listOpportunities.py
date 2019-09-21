import pytest

from ...app.entities.opportunity import Opportunity
from ...app.utils.exceptions import ArgumentException
from ...app.services.opportunity.listOpportunitiesService import ListOpportunitiesService

# @TODO: this should be a database test (with a fake databse, maybe a unittest one)
# https://medium.com/@vittorio.camisa/agile-database-integration-tests-with-python-sqlalchemy-and-factory-boy-6824e8fe33a1

class FakeOpportunityRepo:
    def __init__(self):
        self.lat = None
        self.lng = None
        self.keywords = None
        self.filters = []
    def initQuery(self):
        self.__init__()
    def centerQuery(self, lat, lng):
        self.lat = lat
        self.lng = lng
    def executeQuery(self):
        if self.lat is None and self.lng is None and self.keywords is None and len(self.filters) == 0:
            return []
        if self.lat is not None and self.lng is not None:
            return [
                Opportunity("opo1",1),
                Opportunity("opo2",2)
            ]


@pytest.fixture()
def service():
    return ListOpportunitiesService(
        opportunityRepository=FakeOpportunityRepo()
    )


def test_no_arguments(service):
    with pytest.raises(ArgumentException):
        service.call({})


def test_arguments_none(service):
    args = {
        'lat': None,
        'lng': None,
        'keywords': None,
        'filters': []
    }
    results = service.call(args)
    assert len(results) == 0

def test_latlngsearch(service):
    args = {
        'lat': 5.25,
        'lng': 2.29,
        'keywords': None,
        'filters': []
    }
    results = service.call(args)
    assert service.opportunityRepository.lat == 5.25
    assert service.opportunityRepository.lng == 2.29
    assert results[0]['name'] == 'opo1'
    assert results[1]['name'] == 'opo2'
