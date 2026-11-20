# API contract

## Current status

No HTTP API endpoints, server entry point, route definitions, or request/response schemas were present in the inspected source. Therefore, there is no implemented API contract to document. The recommendation engine currently exposes Python functions only. The following is the verified callable interface, not an HTTP endpoint.

## Python service interface

```python
recommend(query: str, products: Iterable[Any], *, api_key: str | None = None,
          max_products: int = 12, max_outfits: int = 3) -> RecommendationResult
```

The result contains:

```text
preferences: StylePreferences
  occasion: string | null
  budget: number | null
  styles: string[]
  colours: string[]
  categories: string[]
  query: string
products: Product[]                  # capped by max_products
outfits: Outfit[]                    # capped by max_outfits
explanation: string
source: "deterministic" | "gemini"
```

Product output fields include `id`, `name`, normalized `category`, `price`, `material`, `rating`, `colour`, `style`, `occasion`, `simulated`, `score`, and `reason`. Outfit output fields are `product_ids`, `products`, `total_price`, and `reason`. Optional source fields vary; the service accepts common aliases such as `current_price`, `product_id`, `title`, `color`, `is_available`, and `stock_quantity`.

## HTTP endpoints

None verified. Do not treat proposed paths such as `/api/recommendations` as implemented. HTTP methods, authentication, error formats, pagination, and status codes remain to be designed and confirmed by developers.

## Frontend-backend integration

No frontend code or integration was available. A future integration needs an agreed HTTP schema, validation/error behavior, product data source, and response mapping. The UI must not imply live prices or inventory when using the demo seed records, which are simulated.
