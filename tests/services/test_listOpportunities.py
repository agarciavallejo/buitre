import pytest

from ...app.utils.exceptions import ArgumentException
from ...app.services.opportunity.listOpportunitiesService import ListOpportunitiesService


class FakeOpportunityRepo:
    def __init__(self):
        pass

    def searchByLatLng(self, lat, lng):
        return []


@pytest.fixture()
def service():
    return ListOpportunitiesService(
        opportunityRepository=FakeOpportunityRepo()
    )


def test_searchbylatlng(service):
    results = service.call(5.2333, 2.4444)
    assert results.length == 0
