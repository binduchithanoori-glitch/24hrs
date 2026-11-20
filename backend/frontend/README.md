# Frontend integration

The frontend can call the FastAPI backend at `http://127.0.0.1:8000` during local development. Set this as the API base URL in the frontend. CORS origins are configured in the project `.env` with a comma-separated `CORS_ORIGINS` list; add the frontend's exact origin there and restart the backend.

Useful routes include `GET /api/products`, `GET /api/products/search?category=Dresses&color=Sage&max_price=100`, `POST /api/users`, `PUT /api/users/{user_id}`, and `POST /api/stylist/recommend`.

Example JSON recommendation request:

```json
{
  "category": "Dresses",
  "occasion": "Party",
  "colors": ["Rose", "Burgundy"],
  "size": "M",
  "min_budget": 30,
  "max_budget": 120,
  "style_preferences": ["floral", "relaxed"]
}
```

Every request and response is documented in `http://127.0.0.1:8000/docs` when the backend is running.
