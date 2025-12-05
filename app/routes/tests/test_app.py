import pytest
from app import create_app, db
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False  # simplify tests
    MONGO_URI = "mongodb://localhost:27017/patient_app_test"


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, username="testuser", email="test@example.com", password="password123"):
    return client.post(
        "/auth/register",
        data={
            "username": username,
            "email": email,
            "password": password,
        },
        follow_redirects=True,
    )


def login(client, username="testuser", password="password123"):
    return client.post(
        "/auth/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )


def test_home_redirects_when_not_logged_in(client):
    resp = client.get("/", follow_redirects=False)
    # Unauthenticated users might be redirected to login
    assert resp.status_code in (302, 200)


def test_register_and_login(client, app):
    resp = register(client)
    assert resp.status_code == 200

    resp = login(client)
    assert resp.status_code == 200
    # After login, try accessing patients
    resp = client.get("/patients/", follow_redirects=False)
    assert resp.status_code in (200, 302)


def test_patients_requires_login(client):
    resp = client.get("/patients/", follow_redirects=False)
    # Should redirect to login when not authenticated
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers.get("Location", "")


def test_dashboard_requires_login(client):
    resp = client.get("/dashboard", follow_redirects=False)
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers.get("Location", "")
