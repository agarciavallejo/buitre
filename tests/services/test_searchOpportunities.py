import pytest

from ...app.services.opportunity.searchOpportunitiesService import SearchOpportunitiesService


@pytest.fixture()
def service():
    return SearchOpportunitiesService()


def test_arguments(service):
    pass
