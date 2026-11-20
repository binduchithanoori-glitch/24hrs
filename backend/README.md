# LookLoom AI

LookLoom AI is a beginner-friendly smart shopping backend. It provides product discovery, basic user style profiles, and a rule-based stylist that ranks suitable in-stock products without external AI services.

## Features and stack

- FastAPI, Python 3.11+, Pydantic, SQLAlchemy, SQLite, and Uvicorn
- Product listing, search, filters, and detail lookup
- User creation and preference updates
- Rule-based recommendations using category, occasion, colors, size, budget, and style keywords
- Startup table creation and one-time catalog seeding
- CORS settings from environment variables

## Project layout

```text
backend/app/       API routes, configuration, database, models, schemas, services
backend/seed/      Sample product catalog
backend/tests/     API tests using isolated in-memory SQLite
docs/              API, schema, and architecture notes
frontend/           Frontend connection notes
```

## Setup and run

In VS Code PowerShell:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item ..\.env.example ..\.env
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` for the welcome response and `http://127.0.0.1:8000/docs` for Swagger. The database defaults to `backend/stylora.db` and is created at startup. Set `APP_NAME`, `DATABASE_URL`, `DEBUG`, and comma-separated `CORS_ORIGINS` in `.env` as needed.

## Tests

From `backend/`, install the requirements above and run:

```powershell
python -m pytest
```

Tests use a temporary in-memory SQLite database and do not modify the development database.

## Main endpoints

- `GET /` and `GET /health`
- `GET /api/products`, `GET /api/products/search`, `GET /api/products/{product_id}`
- `POST /api/users`, `GET /api/users/{user_id}`, `PUT /api/users/{user_id}`
- `POST /api/stylist/recommend`

See [docs/API_CONTRACT.md](docs/API_CONTRACT.md) for request and response details.
