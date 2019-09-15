import pytest

from ...app.utils.exceptions import ArgumentException
from ...app.services.opportunity.searchOpportunitiesService import SearchOpportunitiesService


@pytest.fixture()
def service():
    return SearchOpportunitiesService()


def test_arguments(service):
    with pytest.raises(ArgumentException):
        service()
