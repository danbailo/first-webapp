import pytest


@pytest.fixture
def client():
    return "my first test using pytest"


def test_client(client):
    assert client == "my first test using pytesta"