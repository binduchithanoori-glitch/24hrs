# Database schema

## Status and scope

The styling engine does not read from or write to a database. A separate adjacent `Stylora-database` checkout contains SQLAlchemy models and an initializer. The schema below documents those files as a separate prototype; its relationship to the Stylora recommendation service is unconfirmed. Do not infer that the engine's demo products are persisted in these tables.

## `products`

| Field | Type | Constraints / notes |
|---|---|---|
| `id` | Integer | Primary key; indexed |
| `name` | String(200) | Required; indexed |
| `category` | String(80) | Required; indexed |
| `occasion` | String(100) | Required; indexed |
| `color` | String(80) | Required; indexed |
| `size` | String(80) | Required; defaults to `One Size` |
| `price` | Float | Required; indexed |
| `description` | Text | Required |
| `image_url` | String(1000) | Required |
| `created_at` | DateTime | Required; database server default `now()` |

Indexes declared: `(category, occasion)` and `(color, size)`; individual indexes are also declared for `id`, `name`, `category`, `occasion`, and `price`.

## `users`

| Field | Type | Constraints / notes |
|---|---|---|
| `id` | Integer | Primary key; indexed |
| `name` | String(200) | Required |
| `email` | String(320) | Required; unique and indexed |
| `preferred_category` | String(80) | Nullable |
| `preferred_color` | String(80) | Nullable |
| `preferred_size` | String(80) | Nullable |
| `budget` | Float | Nullable |
| `created_at` | DateTime | Required; database server default `now()` |

## Relationships

No foreign keys or ORM relationships are declared between `users` and `products`, and no order, saved outfit, or preference-history table is present. The initializer creates tables and inserts seed products if a matching name/category/occasion record does not already exist.

## Database configuration

The separate prototype uses SQLite at `backend/bestpick.db` by default and accepts `DATABASE_URL` as an override. The model and seed names (`Product`, `User`, `products.json`) are verified in that checkout; the database has not been shown to serve the recommendation engine.
