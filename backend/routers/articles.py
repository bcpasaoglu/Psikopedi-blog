from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from sqlalchemy.orm import Session

from .. import repository
from ..categories import CATEGORIES
from ..schemas import ArticleOut, CategoryOut

router = APIRouter(prefix="/api", tags=["articles"])


async def get_db(request: Request):
    # Endpoints below read inside `with db.begin()`: ending the transaction
    # returns the connection to the pool before the response is serialized,
    # which for sync endpoints waits for a free worker thread. Holding the
    # connection through that wait exhausted the pool under ~100 concurrent
    # requests and deadlocked until the pool timeout.
    async for db in request.app.state.get_db():
        yield db


@router.get("/articles", response_model=list[ArticleOut])
def list_articles(
    response: Response,
    q: str | None = Query(default=None, max_length=100, description="Search in title, summary and content"),
    category: str | None = Query(default=None, max_length=50, description="Filter by category slug"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    """List articles, newest first. The total count is returned in `X-Total-Count`."""
    with db.begin():
        rows, total = repository.list_articles(db, q, limit, offset, category)
    response.headers["X-Total-Count"] = str(total)
    return rows


@router.get("/articles/{id_or_slug}", response_model=ArticleOut)
def get_article(id_or_slug: str, db: Session = Depends(get_db)):
    """Return a single article by numeric id or slug."""
    with db.begin():
        article = repository.get_by_id_or_slug(db, id_or_slug)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    """All categories with the number of published articles in each."""
    with db.begin():
        counts = repository.category_counts(db)
    return [
        CategoryOut(slug=c.slug, name=c.name, description=c.description, count=counts.get(c.slug, 0))
        for c in CATEGORIES
    ]
