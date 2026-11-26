from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import repository
from ..models import Article
from ..schemas import ArticleCreate, ArticleOut, ArticleUpdate
from ..security import require_admin
from .articles import get_db

router = APIRouter(prefix="/api/admin/articles", tags=["admin"], dependencies=[Depends(require_admin)])


def _get_or_404(db: Session, item_id: int) -> Article:
    article = db.get(Article, item_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.post("", response_model=ArticleOut, status_code=status.HTTP_201_CREATED)
def create_article(payload: ArticleCreate, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude={"slug"})
    data["date"] = payload.date or date.today()
    article = Article(slug=repository.unique_slug(db, payload.slug or payload.title), **data)
    db.add(article)
    db.commit()
    return article


@router.patch("/{item_id}", response_model=ArticleOut)
def update_article(item_id: int, payload: ArticleUpdate, db: Session = Depends(get_db)):
    article = _get_or_404(db, item_id)
    changes = payload.model_dump(exclude_unset=True, exclude={"slug"})
    # Slug: explicit slug wins, otherwise regenerate when the title changes.
    if payload.slug:
        article.slug = repository.unique_slug(db, payload.slug, exclude_id=item_id)
    elif "title" in changes and changes["title"] != article.title:
        article.slug = repository.unique_slug(db, changes["title"], exclude_id=item_id)
    for field, value in changes.items():
        if value is not None:
            setattr(article, field, value)
    db.commit()
    return article


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(item_id: int, db: Session = Depends(get_db)):
    db.delete(_get_or_404(db, item_id))
    db.commit()
