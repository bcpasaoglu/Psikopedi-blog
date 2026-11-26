# PsikopediBlog

A Turkish-language blog platform focused on psychology, personal growth, and mental health.

Built with a comic book-inspired UI, smooth GSAP animations, and a FastAPI backend serving both the API and the static frontend from a single origin.

![Status](https://img.shields.io/badge/Status-Work%20in%20Progress-orange)
![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.129-009688?logo=fastapi&logoColor=white)
[![CI](https://github.com/bcpasaoglu/Psikopedi-blog/actions/workflows/ci.yml/badge.svg)](https://github.com/bcpasaoglu/Psikopedi-blog/actions/workflows/ci.yml)
![License](https://img.shields.io/badge/License-MIT-green)

> **Note:** This project is under active development. Features and API may change.

---

## Project Structure

```
backend/
  main.py                 # FastAPI app, article endpoints, static file serving

frontend/
  index.html              # Landing page with blog card list
  article.html            # Single article view (fetched via API)
  script.js               # Shared JS — theme toggle, GSAP animations, article rendering
  style.css               # Comic book theme (halftone patterns, bold borders, speech bubbles)
```

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/articles` | List all articles |
| GET | `/api/articles/{id_or_slug}` | Single article by numeric ID or slug |
| POST | `/api/admin/articles` | Create an article (admin) |
| PUT | `/api/admin/articles/{id}` | Update an article (admin) |
| DELETE | `/api/admin/articles/{id}` | Delete an article (admin) |

Admin endpoints require the `X-Admin-Token` header to match the `ADMIN_TOKEN` environment variable. If `ADMIN_TOKEN` is not set, the admin API is disabled and returns `503` (fail closed).

## Running Locally

```bash
pip install -r requirements.txt
echo "ADMIN_TOKEN=change-me" > .env
uvicorn backend.main:app --reload
# open http://localhost:8000
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

Tests run on every push and pull request via GitHub Actions.

## Tech Stack

**Backend** — FastAPI, Uvicorn, python-dotenv

**Frontend** — Vanilla JS, GSAP for animations, DOMPurify for XSS protection

## Roadmap

- [ ] SQLite database integration
- [x] Admin endpoints protected by a token (fail closed)
- [x] Automated tests and CI
- [ ] Admin authentication (JWT)
- [ ] Article CRUD operations
- [ ] Categories and tags
- [ ] Search

## License

MIT
