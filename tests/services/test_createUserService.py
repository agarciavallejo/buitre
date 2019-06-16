import pytest
import mocker


def test_emailless_call_raises_exception(mocker):
    mocker.patch.object(CreateUserService, 'call')
