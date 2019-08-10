import pytest

from ...app.utils.exceptions import ArgumentException
from ...app.services.profile.updateUserTags import UpdateUserTags

@pytest.fixture
def service():
    service = UpdateUserTags()
    return service

def test_arguments(service):
    with pytest.raises(ArgumentException):
        service.call({})