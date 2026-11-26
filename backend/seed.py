"""Sample articles inserted into an empty database so the site is never blank."""

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import Article

SAMPLE_ARTICLES = [
    {
        "slug": "basarinin-psikolojisi-kucuk-adimlarin-gucu",
        "title": "Başarının Psikolojisi: Küçük Adımların Gücü",
        "date": date(2026, 2, 22),
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
        "slug": "stresle-basa-cikmanin-yollari",
        "title": "Stresle Başa Çıkmanın Yolları",
        "date": date(2026, 1, 15),
        "summary": "Günlük hayatın stresiyle başa çıkmak için etkili stratejiler.",
        "content": (
            "Stres yönetimi, nefes teknikleri ve günlük pratiklerle hayat kalitenizi artırır. "
            "Bu yazıda kısa ve uygulanabilir yöntemlerden bahsedeceğiz."
        ),
        "image_url": "https://picsum.photos/1200/500?random=21",
    },
]


def seed_if_empty(db: Session) -> int:
    if db.scalar(select(func.count()).select_from(Article)):
        return 0
    db.add_all(Article(author="Psikopedi", **data) for data in SAMPLE_ARTICLES)
    db.commit()
    return len(SAMPLE_ARTICLES)
