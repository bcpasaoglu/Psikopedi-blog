# PsikopediBlog

A Turkish-language blog platform focused on psychology, personal growth, and mental health.

Built with a comic book-inspired UI, smooth GSAP animations, and a FastAPI backend serving both the API and the static frontend from a single origin.

![Status](https://img.shields.io/badge/Status-Work%20in%20Progress-orange)
![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.129-009688?logo=fastapi&logoColor=white)
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

## Tech Stack

**Backend** — FastAPI, Uvicorn, python-dotenv

**Frontend** — Vanilla JS, GSAP for animations, DOMPurify for XSS protection

## Roadmap

- [ ] SQLite database integration
- [ ] Admin authentication (JWT)
- [ ] Article CRUD operations
- [ ] Categories and tags
- [ ] Search

## License

MIT
