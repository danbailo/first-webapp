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


def test_status_code(client):
    response = client.get("/")
    assert response.status_code == 200


def test_check_register(client):
    response = client.get("/")
    assert "Register" in response.get_data(as_text=True)


def test_check_login(client):
    response = client.get("/")
    assert "Login" in response.get_data(as_text=True)
