import pytest
import sys
sys.path.append('../')
from app import create_app, db


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" # in memory
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config['WTF_CSRF_ENABLED'] = False
    context = app.app_context()
    context.push()

    db.create_all()

    yield app.test_client()

    db.session.remove()
    db.drop_all()
    context.pop()

# unit tests


def test_status_code(client):
    response = client.get("/")
    assert response.status_code == 200


def test_check_register(client):
    response = client.get("/")
    assert "Register" in response.get_data(as_text=True)


def test_check_login(client):
    response = client.get("/")
    assert "Login" in response.get_data(as_text=True)

# in this mode, the crfs token must be disable
# unit test with db integration


def test_register_user(client):
    response = client.post("/register", data={
        "name": "test",
        "email": "test@email.com",
        "password": "1234",
    }, follow_redirects=True)

    assert "test" in response.get_data(as_text=True)


def test_login_user(client):
    response = client.post("/login", data={
        "email": "test@email.com",
        "password": "1234",
    }, follow_redirects=True)

    assert "/login" in response.get_data(as_text=True)
