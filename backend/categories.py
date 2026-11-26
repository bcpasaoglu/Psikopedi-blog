"""Fixed list of blog categories.

Categories are a small, editorial set, so they live in code instead of a table;
articles reference them by slug.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
    slug: str
    name: str
    description: str


CATEGORIES: tuple[Category, ...] = (
    Category("kaygi-ve-stres", "Kaygı & Stres", "Kaygıyı anlamak ve stresle baş etmek"),
    Category("kisisel-gelisim", "Kişisel Gelişim", "Alışkanlıklar, motivasyon ve hedefler"),
    Category("iliskiler", "İlişkiler", "Aile, arkadaşlık ve partner ilişkileri"),
    Category("uyku-ve-beden", "Uyku & Beden", "Zihin ile beden arasındaki bağ"),
    Category("farkindalik", "Farkındalık", "Şimdiki ana dönmek ve öz şefkat"),
)
DEFAULT_CATEGORY = "kisisel-gelisim"
CATEGORY_SLUGS = frozenset(c.slug for c in CATEGORIES)
