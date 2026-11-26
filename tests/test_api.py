import pytest
from fastapi.testclient import TestClient

from backend import main

TOKEN = "test-token"
NEW_ARTICLE = {"title": "Kaygı ve Uyku İlişkisi", "summary": "Kısa özet", "content": "İçerik"}


@pytest.fixture
def client(monkeypatch):
    original = [dict(a) for a in main.ARTICLES]
    monkeypatch.setenv("ADMIN_TOKEN", TOKEN)
    yield TestClient(main.app)
    main.ARTICLES[:] = original


def auth(token=TOKEN):
    return {"X-Admin-Token": token}


def test_list_articles(client):
    res = client.get("/api/articles")
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_get_article_by_id_and_slug(client):
    first = client.get("/api/articles").json()[0]
    assert client.get(f"/api/articles/{first['id']}").json()["slug"] == first["slug"]
    assert client.get(f"/api/articles/{first['slug']}").json()["id"] == first["id"]


def test_get_missing_article_returns_404(client):
    assert client.get("/api/articles/does-not-exist").status_code == 404


def test_admin_disabled_without_token_config(client, monkeypatch):
    monkeypatch.delenv("ADMIN_TOKEN")
    res = client.post("/api/admin/articles", json=NEW_ARTICLE)
    assert res.status_code == 503


@pytest.mark.parametrize("headers", [{}, {"X-Admin-Token": "wrong"}])
def test_admin_rejects_missing_or_wrong_token(client, headers):
    res = client.post("/api/admin/articles", json=NEW_ARTICLE, headers=headers)
    assert res.status_code == 401


def test_create_update_delete_article(client):
    created = client.post("/api/admin/articles", json=NEW_ARTICLE, headers=auth())
    assert created.status_code == 200
    art = created.json()
    assert art["slug"] == "kaygi-ve-uyku-iliskisi"

    updated = client.put(f"/api/admin/articles/{art['id']}", json={"title": "Yeni Başlık"}, headers=auth())
    assert updated.json()["slug"] == "yeni-baslik"

    deleted = client.delete(f"/api/admin/articles/{art['id']}", headers=auth())
    assert deleted.json()["ok"] is True
    assert client.get(f"/api/articles/{art['id']}").status_code == 404


def test_duplicate_titles_get_unique_slugs(client):
    a = client.post("/api/admin/articles", json=NEW_ARTICLE, headers=auth()).json()
    b = client.post("/api/admin/articles", json=NEW_ARTICLE, headers=auth()).json()
    assert a["slug"] != b["slug"]
    assert b["slug"].endswith("-2")


def test_slugify_handles_turkish_characters():
    assert main.slugify("Çocuklarda Öğrenme Güçlüğü") == "cocuklarda-ogrenme-guclugu"
    assert main.slugify("!!!") == "makale"
