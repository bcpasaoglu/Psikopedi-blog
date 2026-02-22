import os
import re
from datetime import date
from typing import Optional
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pathlib import Path
from pydantic import BaseModel

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

app = FastAPI(title="Psychology Blog API", version="1.0")

cors_origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample in-memory articles (would come from a database in a real app)
ARTICLES = [
    {
        "id": 1,
        "slug": "basarinin-psikolojisi-kucuk-adimlarin-gucu",
        "title": "Başarının Psikolojisi: Küçük Adımların Gücü",
        "author": "Psikopedi",
        "date": "2026-02-22",
        "summary": "Başarıya giden yolda küçük adımların önemini keşfedin.",
        "content": (
            "Başarı, büyük hedeflere ulaşmak için atılan küçük adımların toplamıdır. "
            "Bu makalede, başarıya giden yolda küçük adımların nasıl büyük farklar yaratabileceğini keşfedeceğiz. "
            "Küçük adımlar, motivasyonu artırır, özgüveni güçlendirir ve sürdürülebilir başarı için sağlam bir temel oluşturur. "
            "Başarıya giden yolculuğunuzda küçük adımların gücünü keşfetmeye hazır olun!"
        ),
        "image_url": "https://picsum.photos/1200/500?random=20",
    },
    {
        "id": 2,
        "slug": "stresle-basa-cikmanin-yollari",
        "title": "Stresle Başa Çıkmanın Yolları",
        "author": "Psikopedi",
        "date": "2026-01-15",
        "summary": "Günlük hayatın stresiyle başa çıkmak için etkili stratejiler.",
        "content": (
            "Stres yönetimi, nefes teknikleri ve günlük pratiklerle hayat kalitenizi artırır. "
            "Bu yazıda kısa ve uygulanabilir yöntemlerden bahsedeceğiz."
        ),
        "image_url": "https://picsum.photos/1200/500?random=21",
    },
]


@app.get("/api/articles")
def get_articles():
    """Return all articles."""
    return ARTICLES


@app.get("/api/articles/{id_or_slug}")
def get_article(id_or_slug: str):
    """Return a single article by numeric id or slug."""
    for a in ARTICLES:
        if str(a.get("id")) == id_or_slug or a.get("slug") == id_or_slug:
            return a
    raise HTTPException(status_code=404, detail="Article not found")


# ── Admin endpoints (simple in-memory CRUD with header token) ─────────────

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "")


def require_admin(x_admin_token: Optional[str] = Header(default=None, alias="X-Admin-Token")):
    if ADMIN_TOKEN:
        if not x_admin_token or x_admin_token != ADMIN_TOKEN:
            raise HTTPException(status_code=401, detail="Unauthorized")
    # if no ADMIN_TOKEN is configured, allow all (dev mode)


def slugify(text: str) -> str:
    text = text.strip().lower()
    # replace Turkish characters roughly and non-alnum with dashes
    mapping = str.maketrans({
        "ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u",
        "Ç": "c", "Ğ": "g", "İ": "i", "Ö": "o", "Ş": "s", "Ü": "u",
    })
    text = text.translate(mapping)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "makale"


class ArticleIn(BaseModel):
    title: str
    author: Optional[str] = "Admin"
    date: Optional[str] = None  # ISO string
    summary: Optional[str] = ""
    content: Optional[str] = ""
    image_url: Optional[str] = ""
    slug: Optional[str] = None


def next_id() -> int:
    return (max((int(a.get("id", 0)) for a in ARTICLES), default=0) + 1) if ARTICLES else 1


@app.post("/api/admin/articles")
def create_article(payload: ArticleIn, _=Depends(require_admin)):
    new_id = next_id()
    slug = payload.slug or slugify(payload.title)
    # ensure unique slug
    existing_slugs = {a.get("slug") for a in ARTICLES}
    base_slug, k = slug, 2
    while slug in existing_slugs:
        slug = f"{base_slug}-{k}"
        k += 1

    article = {
        "id": new_id,
        "slug": slug,
        "title": payload.title,
        "author": payload.author or "Admin",
        "date": payload.date or date.today().isoformat(),
        "summary": payload.summary or "",
        "content": payload.content or "",
        "image_url": payload.image_url or "",
    }
    ARTICLES.append(article)
    return article


@app.put("/api/admin/articles/{item_id}")
def update_article(item_id: int, payload: ArticleIn, _=Depends(require_admin)):
    for a in ARTICLES:
        if int(a.get("id")) == item_id:
            old_title = a.get("title")
            # slug: explicit slug > auto-generate if title changed > keep existing
            if payload.slug:
                a["slug"] = payload.slug
            elif payload.title and payload.title != old_title:
                a["slug"] = slugify(payload.title)
            a.update({
                "title": payload.title or a["title"],
                "author": payload.author or a.get("author", "Admin"),
                "date": payload.date or a.get("date"),
                "summary": payload.summary if payload.summary is not None else a.get("summary", ""),
                "content": payload.content if payload.content is not None else a.get("content", ""),
                "image_url": payload.image_url if payload.image_url is not None else a.get("image_url", ""),
            })
            return a
    raise HTTPException(status_code=404, detail="Article not found")


@app.delete("/api/admin/articles/{item_id}")
def delete_article(item_id: int, _=Depends(require_admin)):
    idx = next((i for i, a in enumerate(ARTICLES) if int(a.get("id")) == item_id), -1)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Article not found")
    art = ARTICLES.pop(idx)
    return {"ok": True, "deleted": art}

# Hatalı linkleri düzeltmek için yönlendirme: /frontend/admin_panel.html -> /admin_panel.html
@app.get("/frontend/admin_panel.html")
def redirect_admin_path():
    return RedirectResponse(url="/admin_panel.html")

# Mount frontend static files so the site is served at the server root
frontend_path = Path(__file__).resolve().parents[1] / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
