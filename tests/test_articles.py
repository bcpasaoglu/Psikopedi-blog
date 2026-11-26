from fastapi.testclient import TestClient

from backend.main import create_app

from .conftest import make_settings


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_sample_articles_are_seeded_newest_first(client):
    res = client.get("/api/articles")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2
    assert res.headers["X-Total-Count"] == "2"
    assert data[0]["date"] >= data[1]["date"]


def test_get_article_by_id_and_slug(client):
    first = client.get("/api/articles").json()[0]
    assert client.get(f"/api/articles/{first['id']}").json()["slug"] == first["slug"]
    assert client.get(f"/api/articles/{first['slug']}").json()["id"] == first["id"]


def test_get_missing_article_returns_404(client):
    assert client.get("/api/articles/does-not-exist").status_code == 404
    assert client.get("/api/articles/9999").status_code == 404


def test_pagination(client):
    page = client.get("/api/articles", params={"limit": 1, "offset": 1})
    assert len(page.json()) == 1
    assert page.headers["X-Total-Count"] == "2"
    assert client.get("/api/articles", params={"limit": 0}).status_code == 422


def test_search(client):
    res = client.get("/api/articles", params={"q": "nefes"})
    assert [a["slug"] for a in res.json()] == ["stresle-basa-cikmanin-yollari"]
    assert client.get("/api/articles", params={"q": "yokboyle"}).json() == []


def test_data_persists_across_app_restarts(tmp_path, auth_headers, client):
    created = client.post("/api/admin/articles", json={"title": "Kalıcı Yazı"}, headers=auth_headers).json()
    with TestClient(create_app(make_settings(tmp_path))) as restarted:
        assert restarted.get(f"/api/articles/{created['slug']}").status_code == 200
        assert restarted.get("/api/articles").headers["X-Total-Count"] == "3"


def test_seeding_can_be_disabled(tmp_path):
    with TestClient(create_app(make_settings(tmp_path, seed_sample_data=False))) as c:
        assert c.get("/api/articles").json() == []


def test_frontend_is_served(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]
