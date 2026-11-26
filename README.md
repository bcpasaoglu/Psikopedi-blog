# Psikopedi Blog

A Turkish-language psychology blog: a **FastAPI + SQLAlchemy** REST API with JWT-protected admin endpoints, serving a comic book-styled vanilla JS frontend from the same origin.

[![CI](https://github.com/bcpasaoglu/Psikopedi-blog/actions/workflows/ci.yml/badge.svg)](https://github.com/bcpasaoglu/Psikopedi-blog/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

## Screenshots

![Home page: category cards with live counts, hero illustration and calls to action](docs/screenshots/home.png)

| Desktop demo | Mobile demo |
|---|---|
| ![Filtering by category, searching and opening an article](docs/screenshots/demo-desktop.gif) | ![Swiping the category strip and scrolling on a phone](docs/screenshots/demo-mobile.gif) |

| Article page | Mobile |
|---|---|
| ![Single article view](docs/screenshots/article.png) | ![Home page on a phone](docs/screenshots/mobile.png) |

<details>
<summary>Full home page and API docs</summary>

![Full home page with the article grid](docs/screenshots/home-full.png)

![Swagger UI with public, auth and JWT-protected admin endpoints](docs/screenshots/api-docs.png)

</details>

All illustrations are original SVGs drawn for this project (`frontend/illustrations.js`); articles without a cover image use their category's illustration.

## Features

- **REST API** for articles with search (`?q=`), category filter (`?category=`), pagination (`?limit=&offset=`), lookup by id or slug, and categories with live counts
- **Persistent storage** with SQLAlchemy 2.0 (SQLite by default, any SQLAlchemy URL via `DATABASE_URL`)
- **Admin authentication**: username + bcrypt password hash exchanged for a short-lived **JWT** (HS256)
- **Fails closed**: the admin API returns `503` until credentials and a JWT secret are configured
- **Login rate limiting**: 5 failed attempts per IP per 5 minutes, then `429` with `Retry-After`
- **Security headers**: Content-Security-Policy (no inline scripts on the site), `X-Frame-Options`, `nosniff`, `Referrer-Policy`, `Permissions-Policy`, optional HSTS
- **Load tested**: a concurrency-100 load test runs in CI (it caught and now guards against a connection pool deadlock)
- **Turkish-aware slugs** (`"Kaygı ve Uyku İlişkisi"` → `kaygi-ve-uyku-iliskisi`), unique per article
- **Input validation** with Pydantic (lengths, dates, no `javascript:` image URLs); frontend renders article HTML through DOMPurify
- **Tested**: 43 pytest tests on an isolated SQLite database per test, run in CI on Python 3.11 to 3.13 with Ruff lint/format checks
- **Frontend**: dependency-free ES modules, comic-style design with original SVG illustrations, responsive down to phone width, keyboard focus styles and reduced-motion support
- **Containerized**: slim, non-root Docker image with a health check, plus a Render Blueprint for one-click deploys

## Architecture

```mermaid
flowchart LR
    Browser -- "HTML / JS / CSS" --> Static[StaticFiles /]
    Browser -- "JSON /api/*" --> Routers
    subgraph FastAPI app
        Routers[articles · auth · admin routers] --> Security[JWT + bcrypt]
        Routers --> Repo[repository.py]
        Repo --> ORM[SQLAlchemy models]
    end
    ORM --> DB[(SQLite / Postgres)]
```

```
backend/
  main.py            # create_app() factory: middleware, routers, static frontend
  config.py          # Settings from env vars / .env (pydantic-settings)
  database.py        # engine, session factory, per-request session dependency
  models.py          # Article ORM model
  schemas.py         # Pydantic request/response models
  repository.py      # queries: list/search/paginate, slug uniqueness
  security.py        # bcrypt verification, JWT issue/verify, admin dependency
  seed.py            # sample articles for an empty database
  categories.py      # fixed category list
  ratelimit.py       # failed-login limiter
  headers.py         # security headers middleware
  hash_password.py   # CLI to generate ADMIN_PASSWORD_HASH
  routers/           # articles.py (public), auth.py, admin.py
frontend/
  index.html, article.html   # pages
  home.js, article.js        # page logic (ES modules, no build step)
  app.js                     # shared API + rendering helpers
  illustrations.js           # original cartoon SVGs per category
  style.css                  # comic-style theme
scripts/load_test.py # concurrent load test used in CI
tests/               # pytest suite
```

The app is built by a factory (`create_app(settings)`), so tests create a fresh app with their own temporary database instead of patching globals.

## API

Interactive docs are available at `/docs` (Swagger UI) when the server is running.

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/health` | | Health check |
| GET | `/api/articles?q=&category=&limit=20&offset=0` | | List articles, newest first. Total in `X-Total-Count` |
| GET | `/api/articles/{id_or_slug}` | | Single article (includes `reading_minutes`) |
| GET | `/api/categories` | | Categories with article counts |
| POST | `/api/auth/login` | | `{"username", "password"}` → `{"access_token", "token_type", "expires_in"}` |
| GET | `/api/auth/me` | Bearer | Current admin |
| POST | `/api/admin/articles` | Bearer | Create an article (`201`) |
| PATCH | `/api/admin/articles/{id}` | Bearer | Partial update; slug is regenerated when the title changes |
| DELETE | `/api/admin/articles/{id}` | Bearer | Delete an article (`204`) |

Example:

```bash
TOKEN=$(curl -s -X POST localhost:8000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"<your password>"}' | jq -r .access_token)

curl -X POST localhost:8000/api/admin/articles \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"title":"Öz Şefkat Nedir?","summary":"Kısa özet","content":"<p>İçerik</p>"}'
```

## Running Locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
python -m backend.hash_password          # paste the output into ADMIN_PASSWORD_HASH
python -c "import secrets; print(secrets.token_urlsafe(48))"   # paste into JWT_SECRET
uvicorn backend.main:app --reload
# open http://localhost:8000
```

Without the admin settings the public site and API work normally; only login and admin endpoints are disabled.

### Docker

```bash
docker build -t psikopedi-blog .
docker run -p 8000:8000 --env-file .env -v psikopedi-data:/app/data psikopedi-blog
```

The SQLite file lives in `/app/data`, so mount a volume to keep data between containers.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///psikopedi.db` | Any SQLAlchemy URL (install the driver, e.g. `psycopg`, for Postgres) |
| `ADMIN_USERNAME` | | Admin login name |
| `ADMIN_PASSWORD_HASH` | | bcrypt hash from `python -m backend.hash_password` |
| `JWT_SECRET` | | Random secret used to sign tokens |
| `JWT_EXPIRE_MINUTES` | `60` | Token lifetime |
| `CORS_ORIGINS` | | Comma-separated origins, only if the frontend is hosted elsewhere |
| `LOGIN_MAX_ATTEMPTS` / `LOGIN_WINDOW_SECONDS` | `5` / `300` | Failed logins allowed per IP per window |
| `ENABLE_HSTS` | `false` | Send `Strict-Transport-Security` (enable behind HTTPS) |
| `FORWARDED_ALLOW_IPS` | `127.0.0.1` | Uvicorn setting: proxies whose `X-Forwarded-For` is trusted (`*` on Render) |
| `SEED_SAMPLE_DATA` | `true` | Insert sample articles into an empty database |

## Deploying to Render

`render.yaml` is a Render Blueprint: create a new Blueprint from this repository, then set `ADMIN_PASSWORD_HASH` in the dashboard (`JWT_SECRET` is generated automatically). On the free plan the disk is not persistent, so articles reset to the sample data on each deploy; attach a Render disk at `/app/data` or point `DATABASE_URL` at a Postgres database for permanent storage.

## Tests

```bash
pytest            # 43 tests
python scripts/load_test.py http://127.0.0.1:8000 --concurrency 100   # against a running server
ruff check . && ruff format --check .
```

The suite covers public endpoints, categories, search and pagination, persistence across app restarts, the schema upgrade for older databases, login, rate limiting, expired/forged/unsigned tokens, fail-closed configuration, security headers, CRUD, slug uniqueness and input validation.

## Roadmap

- [x] SQLite persistence with SQLAlchemy
- [x] JWT admin authentication
- [x] Search and pagination
- [x] Docker image and Render deploy config
- [x] Categories, login rate limiting, security headers, load test in CI
- [ ] Admin panel UI on top of the JWT API
- [ ] Alembic migrations
- [ ] Tags

## License

MIT
