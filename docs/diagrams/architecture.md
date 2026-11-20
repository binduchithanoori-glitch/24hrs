# Stylora architecture diagram

Solid arrows show the callable flow verified in the styling service. Dashed components are separate or proposed; they are not verified as integrated.

```mermaid
flowchart LR
    Shopper[Shopper]
    UI[Frontend<br/>not present in inspected workspace]
    API[HTTP API<br/>not found]
    Caller[Python caller]
    Engine[recommend(query, products)]
    Parser[Intent parser]
    Gemini[Gemini API<br/>optional via GEMINI_API_KEY]
    Fallback[Deterministic keyword parser]
    Rank[Deterministic filter and ranking]
    Outfit[Outfit builder<br/>dress OR top + bottom<br/>optional finishing items]
    Seed[Demo product JSON<br/>simulated records]
    DB[Separate SQLAlchemy database prototype<br/>SQLite by default; integration unconfirmed]
    Result[RecommendationResult<br/>preferences, products, outfits, explanation, source]

    Shopper -. planned .-> UI
    UI -. planned .-> API
    API -. no route found .-> Engine
    Caller --> Engine
    Seed --> Caller
    Engine --> Parser
    Parser --> Gemini
    Parser --> Fallback
    Gemini --> Parser
    Fallback --> Parser
    Parser --> Rank
    Engine --> Rank
    Rank --> Outfit
    Outfit --> Result
    Rank --> Result
    DB -. no connection found .-> Engine
```
