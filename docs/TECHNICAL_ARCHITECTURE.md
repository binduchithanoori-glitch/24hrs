# Technical architecture

## Evidence boundary

The selected workspace contained no application source. Inspection found a styling engine and demo seed data in the adjacent `Stylora-docs` checkout, plus independent SQLAlchemy models and seed data in the adjacent `Stylora-database` checkout. No frontend source, HTTP routes, or integration between these checkouts was found. The localhost URL on port 3000 was unreachable at inspection time. The architecture below documents these components separately and marks the joins as proposed.

## Frontend architecture

Unknown. No frontend source, package manifest, component tree, or browser-visible interface was available. The URL alone does not establish framework, pages, controls, or behavior. A frontend should submit a request and render results only after an API contract is agreed and implemented.

## Backend architecture

The available Python styling module (`backend/app/services/styling_engine.py` in the adjacent `Stylora-docs` checkout) is a callable service module, not a web application. Its `recommend(query, products)` function parses intent, maps caller-supplied product records into a normalized view, filters and scores candidates, builds outfit combinations, and returns a `RecommendationResult` containing preferences, products, outfits, explanation, and parser source. No request handler or route wraps it in HTTP.

## AI recommendation engine

Intent parsing can call Gemini when `GEMINI_API_KEY` is set. The model name defaults to `gemini-2.0-flash` and can be overridden with `GEMINI_MODEL`. Parsing asks for occasion, budget, styles, colours, and categories. Network errors, malformed output, and other exceptions fall back to deterministic keyword parsing. Ranking and outfit generation are deterministic Python logic; the language model does not supply product facts.

The engine filters invalid prices, unavailable/out-of-stock records, and products above the parsed budget. It scores category, colour, style, occasion, and rating matches, sorts by score then price and identifier, returns up to 12 products by default, and builds up to 3 outfits by default. An outfit base is either one dress or one top plus one bottom; shoes, bags, and accessories are optional additions if they fit the budget.

## Database

No database is connected to the styling engine in the inspected code. A separate adjacent prototype defines SQLAlchemy `Product` and `User` models and defaults to SQLite, with `DATABASE_URL` override and a seed routine. Its names and data model are not demonstrably connected to the recommendation service. See [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md).

## Data flow

Verified service flow: caller supplies query and product iterable → parser extracts preferences → product records are normalized and filtered → deterministic ranking runs → outfit candidates are composed → structured Python result is returned to caller. HTTP transport, database reads, frontend rendering, and external catalog ingestion are not implemented in the inspected files.

## Operational configuration

- `GEMINI_API_KEY`: optional key enabling Gemini intent parsing.
- `GEMINI_MODEL`: optional model override.
- `DATABASE_URL`: used only by the separate database prototype; defaults to a SQLite file under its backend directory.
