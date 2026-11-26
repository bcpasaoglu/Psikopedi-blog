"""Data access for articles, kept separate from the HTTP layer."""

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from .models import Article
from .utils import slugify


def list_articles(db: Session, q: str | None, limit: int, offset: int) -> tuple[list[Article], int]:
    stmt = select(Article)
    if q:
        pattern = f"%{q}%"
        stmt = stmt.where(
            or_(Article.title.ilike(pattern), Article.summary.ilike(pattern), Article.content.ilike(pattern))
        )
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = db.scalars(stmt.order_by(Article.date.desc(), Article.id.desc()).limit(limit).offset(offset)).all()
    return list(rows), total


def get_by_id_or_slug(db: Session, id_or_slug: str) -> Article | None:
    if id_or_slug.isdigit():
        article = db.get(Article, int(id_or_slug))
        if article:
            return article
    return db.scalar(select(Article).where(Article.slug == id_or_slug))


def unique_slug(db: Session, wanted: str, exclude_id: int | None = None) -> str:
    """Return `wanted` (slugified), suffixed with -2, -3, ... if already taken."""
    base = slugify(wanted)
    stmt = select(Article.slug).where(or_(Article.slug == base, Article.slug.like(f"{base}-%")))
    if exclude_id is not None:
        stmt = stmt.where(Article.id != exclude_id)
    taken = set(db.scalars(stmt))
    slug, k = base, 2
    while slug in taken:
        slug = f"{base}-{k}"
        k += 1
    return slug
