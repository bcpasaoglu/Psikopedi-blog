from datetime import UTC, datetime, timedelta

import jwt
import pytest
from fastapi.testclient import TestClient

from backend.main import create_app

from .conftest import ADMIN_PASSWORD, ADMIN_USER, make_settings


def test_login_returns_bearer_token(client):
    res = client.post("/api/auth/login", json={"username": ADMIN_USER, "password": ADMIN_PASSWORD})
    body = res.json()
    assert res.status_code == 200
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == 3600


@pytest.mark.parametrize("username,password", [(ADMIN_USER, "wrong"), ("someone", ADMIN_PASSWORD), ("", "")])
def test_login_rejects_bad_credentials(client, username, password):
    res = client.post("/api/auth/login", json={"username": username, "password": password})
    assert res.status_code == 401


def test_me_requires_token(client, auth_headers):
    assert client.get("/api/auth/me").status_code == 401
    assert client.get("/api/auth/me", headers=auth_headers).json() == {"username": ADMIN_USER}


@pytest.mark.parametrize("missing", ["admin_username", "admin_password_hash", "jwt_secret"])
def test_admin_api_fails_closed_when_not_configured(tmp_path, missing):
    with TestClient(create_app(make_settings(tmp_path, **{missing: ""}))) as c:
        assert c.post("/api/auth/login", json={"username": ADMIN_USER, "password": ADMIN_PASSWORD}).status_code == 503
        assert c.post("/api/admin/articles", json={"title": "x"}).status_code == 503


def _token(settings, **claims):
    payload = {"sub": ADMIN_USER, "exp": datetime.now(UTC) + timedelta(minutes=5)}
    payload.update(claims)
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def test_rejects_expired_token(client, settings):
    token = _token(settings, exp=datetime.now(UTC) - timedelta(seconds=1))
    assert client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_rejects_token_signed_with_other_secret(client):
    token = jwt.encode(
        {"sub": ADMIN_USER, "exp": datetime.now(UTC) + timedelta(minutes=5)}, "other-secret-xxxxxxxxxxxxxxxxxxxxxxxx"
    )
    assert client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_rejects_token_for_other_subject(client, settings):
    token = _token(settings, sub="intruder")
    assert client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_rejects_unsigned_token(client):
    token = jwt.encode({"sub": ADMIN_USER, "exp": 9999999999}, key=None, algorithm="none")
    assert client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401
