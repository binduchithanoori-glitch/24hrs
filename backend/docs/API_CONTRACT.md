# API contract

All request and response bodies use JSON. Invalid inputs return FastAPI's `422` validation response (`{"detail": [...]}`). Missing records return `404` with a short `detail` message.

| Method and path | Purpose |
|---|---|
| `GET /` | Welcome message and running status |
| `GET /health` | Health status |
| `GET /api/products` | List products; supports `limit` (1–200) and `offset` |
| `GET /api/products/search` | Optional `search`, `category`, `color`, `size`, `min_price`, `max_price` filters |
| `GET /api/products/{product_id}` | Product details |
| `POST /api/users` | Create a user; returns `201`, duplicate email returns `409` |
| `GET /api/users/{user_id}` | User profile and saved preferences |
| `PUT /api/users/{user_id}` | Update supplied name or preferences |
| `POST /api/stylist/recommend` | Ranked, explained recommendations |

Search example: `GET /api/products/search?category=Dresses&color=Sage&size=M&min_price=30&max_price=100`. A reversed price range returns `400`.

Create user request:

```json
{"name":"Asha Rao","email":"asha@example.com","favorite_colors":["Navy"],"favorite_categories":["Tops"],"sizes":["M"],"style_preferences":"classic"}
```

Recommendation request:

```json
{"category":"Dresses","occasion":"Party","colors":["Rose"],"size":"M","min_budget":30,"max_budget":120,"style_preferences":["floral"],"limit":10}
```

Response shape:

```json
{"preferences":{"category":"Dresses","occasion":"Party","colors":["Rose"],"size":"M","min_budget":30,"max_budget":120,"style_preferences":["floral"],"limit":10},"recommendations":[{"product":{"id":1,"name":"Floral Party Dress","description":"...","category":"Dresses","occasion":"Party","color":"Rose","sizes":["XS","S","M","L"],"price":98,"image_url":null,"in_stock":true},"score":10,"explanation":"Recommended because it matches your dresses category, suits a party occasion, matches your color choice, is available in size M."}]}
```

Create/update user returns the user with preference arrays. Duplicate email is `409`; missing product or user is `404`.
