# Architecture

```mermaid
flowchart LR
    Frontend[Frontend or API client] --> Routes[FastAPI routes]
    Routes --> Schemas[Pydantic validation and response schemas]
    Routes --> Stylist[Rule-based stylist service]
    Stylist --> Session[Reusable SQLAlchemy session]
    Routes --> Session
    Session --> Models[Product and User models]
    Models --> DB[(SQLite database)]
    Startup[Application startup] --> Session
    Seed[products.json] --> Startup
```

Routes handle HTTP and status codes. Pydantic schemas validate input and shape output. The stylist service scores catalog matches. Database sessions and SQLAlchemy models own persistence. Startup creates tables and seeds an empty product catalog.
