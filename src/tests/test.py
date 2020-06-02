import pytest
import sys
sys.path.append('../')
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    context = app.app_context()
    context.push()

    yield app.test_client()

    context.pop()


def test_client(client):
    request = client.get("/")
    assert request.status_code == 200
