import pytest

from backend.utils import slugify

NEW_ARTICLE = {"title": "Kaygı ve Uyku İlişkisi", "summary": "Kısa özet", "content": "İçerik"}


@pytest.mark.parametrize("headers", [{}, {"Authorization": "Bearer not-a-jwt"}])
def test_admin_rejects_missing_or_invalid_token(client, headers):
    assert client.post("/api/admin/articles", json=NEW_ARTICLE, headers=headers).status_code == 401
    assert client.patch("/api/admin/articles/1", json={"title": "x"}, headers=headers).status_code == 401
    assert client.delete("/api/admin/articles/1", headers=headers).status_code == 401


def test_create_update_delete_article(client, auth_headers):
    created = client.post("/api/admin/articles", json=NEW_ARTICLE, headers=auth_headers)
    assert created.status_code == 201
    art = created.json()
    assert art["slug"] == "kaygi-ve-uyku-iliskisi"
    assert art["author"] == "Psikopedi"

    updated = client.patch(
        f"/api/admin/articles/{art['id']}", json={"title": "Yeni Başlık"}, headers=auth_headers
    ).json()
    assert updated["slug"] == "yeni-baslik"
    assert updated["summary"] == "Kısa özet"  # untouched fields are kept

    assert client.delete(f"/api/admin/articles/{art['id']}", headers=auth_headers).status_code == 204
    assert client.get(f"/api/articles/{art['id']}").status_code == 404


def test_duplicate_titles_get_unique_slugs(client, auth_headers):
    a = client.post("/api/admin/articles", json=NEW_ARTICLE, headers=auth_headers).json()
    b = client.post("/api/admin/articles", json=NEW_ARTICLE, headers=auth_headers).json()
    c = client.post("/api/admin/articles", json=NEW_ARTICLE, headers=auth_headers).json()
    assert [a["slug"], b["slug"], c["slug"]] == [
        "kaygi-ve-uyku-iliskisi",
        "kaygi-ve-uyku-iliskisi-2",
        "kaygi-ve-uyku-iliskisi-3",
    ]


def test_update_cannot_steal_existing_slug(client, auth_headers):
    first = client.get("/api/articles").json()[0]
    new = client.post("/api/admin/articles", json=NEW_ARTICLE, headers=auth_headers).json()
    res = client.patch(f"/api/admin/articles/{new['id']}", json={"slug": first["slug"]}, headers=auth_headers)
    assert res.json()["slug"] == f"{first['slug']}-2"


def test_update_keeps_own_slug(client, auth_headers):
    art = client.post("/api/admin/articles", json=NEW_ARTICLE, headers=auth_headers).json()
    res = client.patch(
        f"/api/admin/articles/{art['id']}", json={"title": NEW_ARTICLE["title"], "content": "x"}, headers=auth_headers
    )
    assert res.json()["slug"] == art["slug"]


def test_missing_article_returns_404(client, auth_headers):
    assert client.patch("/api/admin/articles/9999", json={"title": "x"}, headers=auth_headers).status_code == 404
    assert client.delete("/api/admin/articles/9999", headers=auth_headers).status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {"title": ""},
        {"title": "x" * 201},
        {"title": "ok", "image_url": "javascript:alert(1)"},
        {"title": "ok", "date": "not-a-date"},
    ],
)
def test_create_validates_input(client, auth_headers, payload):
    assert client.post("/api/admin/articles", json=payload, headers=auth_headers).status_code == 422


def test_slugify_handles_turkish_characters():
    assert slugify("Çocuklarda Öğrenme Güçlüğü") == "cocuklarda-ogrenme-guclugu"
    assert slugify("İstanbul'da Işık") == "istanbul-da-isik"
    assert slugify("!!!") == "makale"
