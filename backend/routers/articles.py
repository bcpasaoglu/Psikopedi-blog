from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from sqlalchemy.orm import Session

from .. import repository
from ..schemas import ArticleOut

router = APIRouter(prefix="/api/articles", tags=["articles"])


def get_db(request: Request):
    yield from request.app.state.get_db()


@router.get("", response_model=list[ArticleOut])
def list_articles(
    response: Response,
    q: str | None = Query(default=None, max_length=100, description="Search in title, summary and content"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    """List articles, newest first. The total count is returned in `X-Total-Count`."""
    rows, total = repository.list_articles(db, q, limit, offset)
    response.headers["X-Total-Count"] = str(total)
    return rows


@router.get("/{id_or_slug}", response_model=ArticleOut)
def get_article(id_or_slug: str, db: Session = Depends(get_db)):
    """Return a single article by numeric id or slug."""
    article = repository.get_by_id_or_slug(db, id_or_slug)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
