import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

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


# Mount frontend static files so the site is served at the server root
frontend_path = Path(__file__).resolve().parents[1] / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
