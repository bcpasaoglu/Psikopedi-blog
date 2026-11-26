"""FastAPI application: JSON API under /api, static frontend at the site root."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import BASE_DIR, Settings, get_settings
from .database import Base, make_engine, make_session_factory, session_dependency
from .routers import admin, articles, auth
from .seed import seed_if_empty


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    engine = make_engine(settings.database_url)
    session_factory = make_session_factory(engine)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Tables are created on startup; a migration tool (Alembic) would replace
        # this once the schema starts changing.
        Base.metadata.create_all(engine)
        if settings.seed_sample_data:
            with session_factory() as db:
                seed_if_empty(db)
        yield
        engine.dispose()

    app = FastAPI(title="Psikopedi Blog API", version="2.0", lifespan=lifespan)
    app.state.get_db = session_dependency(session_factory)
    app.dependency_overrides[get_settings] = lambda: settings

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
        expose_headers=["X-Total-Count"],
    )

    @app.get("/api/health", tags=["health"])
    def health():
        return {"status": "ok"}

    app.include_router(articles.router)
    app.include_router(auth.router)
    app.include_router(admin.router)

    frontend_path = BASE_DIR / "frontend"
    if frontend_path.exists():
        app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
    return app


app = create_app()
