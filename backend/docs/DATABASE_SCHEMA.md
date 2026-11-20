# Database schema

SQLAlchemy creates tables at application startup. The default store is SQLite; override `DATABASE_URL` to select another SQLAlchemy-compatible database. On first startup only, products from `backend/seed/products.json` are inserted when the products table is empty.

## Product

`products`: `id` integer primary key; `name`, `description`, `category`, `occasion`, and `color` text fields; `sizes` comma-separated text; `price` float; nullable `image_url`; and `in_stock` boolean. There is no product-to-user relationship in this initial catalog.

## User

`users`: `id` integer primary key; `name` text; unique indexed `email`; comma-separated `favorite_colors`, `favorite_categories`, and `sizes`; and free-text `style_preferences`. User preferences are stored on the profile; no authentication is included.
