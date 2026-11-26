"""SQLAlchemy engine and session handling."""

from collections.abc import AsyncIterator

from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Larger than FastAPI's default 40 worker threads, so a thread holding a session
# never waits for a connection (see routers/articles.py).
POOL_SIZE = 20
MAX_OVERFLOW = 30


class Base(DeclarativeBase):
    pass


def make_engine(database_url: str) -> Engine:
    is_sqlite = database_url.startswith("sqlite")
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False} if is_sqlite else {},
        pool_size=POOL_SIZE,
        max_overflow=MAX_OVERFLOW,
        pool_timeout=10,
        pool_pre_ping=not is_sqlite,
    )
    if is_sqlite:

        @event.listens_for(engine, "connect")
        def _sqlite_pragmas(dbapi_conn, _record):
            cur = dbapi_conn.cursor()
            # WAL lets readers proceed while a write is in progress.
            cur.execute("PRAGMA journal_mode=WAL")
            cur.execute("PRAGMA busy_timeout=5000")
            cur.close()

    return engine


def add_missing_columns(engine: Engine) -> None:
    """Tiny forward-only migration for columns added after the first release.

    create_all() never alters existing tables, so databases created by an older
    version would miss new columns. A real migration tool (Alembic) should take
    over once the schema grows further.
    """
    insp = inspect(engine)
    for table in Base.metadata.sorted_tables:
        if not insp.has_table(table.name):
            continue
        existing = {c["name"] for c in insp.get_columns(table.name)}
        for column in table.columns:
            if column.name in existing:
                continue
            ddl_type = column.type.compile(dialect=engine.dialect)
            default = column.server_default.arg if column.server_default is not None else None
            clause = f" NOT NULL DEFAULT '{default}'" if default is not None else ""
            with engine.begin() as conn:
                conn.execute(text(f'ALTER TABLE {table.name} ADD COLUMN "{column.name}" {ddl_type}{clause}'))


def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def session_dependency(factory: sessionmaker[Session]):
    """Build a FastAPI dependency that yields one session per request.

    Async so that closing the session runs on the event loop instead of queueing
    for one of FastAPI's worker threads under load.
    """

    async def get_db() -> AsyncIterator[Session]:
        db = factory()
        try:
            yield db
        finally:
            db.close()

    return get_db
