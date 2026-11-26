from fastapi.testclient import TestClient

from backend.main import create_app
from backend.seed import SAMPLE_ARTICLES

from .conftest import make_settings


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_sample_articles_are_seeded_newest_first(client):
    res = client.get("/api/articles")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == len(SAMPLE_ARTICLES)
    assert res.headers["X-Total-Count"] == str(len(SAMPLE_ARTICLES))
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
    assert page.headers["X-Total-Count"] == str(len(SAMPLE_ARTICLES))
    assert client.get("/api/articles", params={"limit": 0}).status_code == 422


def test_search(client):
    res = client.get("/api/articles", params={"q": "nefes"})
    assert [a["slug"] for a in res.json()] == ["stresle-basa-cikmanin-yollari"]
    assert client.get("/api/articles", params={"q": "yokboyle"}).json() == []


def test_data_persists_across_app_restarts(tmp_path, auth_headers, client):
    created = client.post("/api/admin/articles", json={"title": "Kalıcı Yazı"}, headers=auth_headers).json()
    with TestClient(create_app(make_settings(tmp_path))) as restarted:
        assert restarted.get(f"/api/articles/{created['slug']}").status_code == 200
        assert restarted.get("/api/articles").headers["X-Total-Count"] == str(len(SAMPLE_ARTICLES) + 1)


def test_seeding_can_be_disabled(tmp_path):
    with TestClient(create_app(make_settings(tmp_path, seed_sample_data=False))) as c:
        assert c.get("/api/articles").json() == []


def test_frontend_is_served(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]


def test_categories_with_counts(client):
    cats = client.get("/api/categories").json()
    assert [c["slug"] for c in cats][:2] == ["kaygi-ve-stres", "kisisel-gelisim"]
    expected = {}
    for a in SAMPLE_ARTICLES:
        expected[a["category"]] = expected.get(a["category"], 0) + 1
    assert {c["slug"]: c["count"] for c in cats if c["count"]} == expected


def test_filter_by_category(client):
    res = client.get("/api/articles", params={"category": "iliskiler"})
    assert res.json() and all(a["category"] == "iliskiler" for a in res.json())
    assert client.get("/api/articles", params={"category": "nope"}).json() == []


def test_reading_time_ignores_html(client):
    art = client.get("/api/articles/oz-sefkat-nedir").json()
    assert art["reading_minutes"] >= 1


def test_security_headers(client):
    res = client.get("/")
    csp = res.headers["Content-Security-Policy"]
    assert "frame-ancestors 'none'" in csp and "'unsafe-inline'" not in csp.split("script-src")[1].split(";")[0]
    assert res.headers["X-Content-Type-Options"] == "nosniff"
    assert res.headers["X-Frame-Options"] == "DENY"
    assert "Strict-Transport-Security" not in res.headers
    # Swagger UI needs its inline bootstrap script.
    assert "'unsafe-inline'" in client.get("/docs").headers["Content-Security-Policy"]


def test_hsts_when_enabled(tmp_path):
    with TestClient(create_app(make_settings(tmp_path, enable_hsts=True))) as c:
        assert c.get("/api/health").headers["Strict-Transport-Security"].startswith("max-age=")


def test_old_database_gets_category_column(tmp_path):
    import sqlite3

    db = tmp_path / "test.db"
    con = sqlite3.connect(db)
    con.execute(
        "CREATE TABLE articles (id INTEGER PRIMARY KEY, slug VARCHAR(200) UNIQUE, title VARCHAR(200), "
        "author VARCHAR(100), date DATE, summary VARCHAR(500), content TEXT, image_url VARCHAR(500), "
        "created_at DATETIME, updated_at DATETIME)"
    )
    con.execute(
        "INSERT INTO articles (slug, title, author, date, summary, content, image_url) "
        "VALUES ('eski', 'Eski', 'A', '2025-01-01', '', '', '')"
    )
    con.commit()
    con.close()
    with TestClient(create_app(make_settings(tmp_path))) as c:
        assert c.get("/api/articles/eski").json()["category"] == "kisisel-gelisim"
