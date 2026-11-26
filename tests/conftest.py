import pytest
from fastapi.testclient import TestClient

from backend.config import Settings
from backend.main import create_app
from backend.security import hash_password

ADMIN_USER = "editor"
ADMIN_PASSWORD = "correct horse battery staple"
_PASSWORD_HASH = hash_password(ADMIN_PASSWORD)


def make_settings(tmp_path, **overrides) -> Settings:
    values = {
        "database_url": f"sqlite:///{tmp_path / 'test.db'}",
        "admin_username": ADMIN_USER,
        "admin_password_hash": _PASSWORD_HASH,
        "jwt_secret": "test-secret-that-is-long-enough-for-hs256",
        "_env_file": None,
    }
    values.update(overrides)
    return Settings(**values)


@pytest.fixture
def settings(tmp_path):
    return make_settings(tmp_path)


@pytest.fixture
def client(settings):
    with TestClient(create_app(settings)) as c:
        yield c


@pytest.fixture
def auth_headers(client):
    res = client.post("/api/auth/login", json={"username": ADMIN_USER, "password": ADMIN_PASSWORD})
    assert res.status_code == 200, res.text
    return {"Authorization": f"Bearer {res.json()['access_token']}"}
