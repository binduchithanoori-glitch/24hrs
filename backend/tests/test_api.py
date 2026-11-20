from contextlib import asynccontextmanager

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db, seed_products
from app.main import app


@pytest.fixture()
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    testing_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.create_all(bind=engine)

    def override_db():
        with testing_session() as db:
            yield db

    @asynccontextmanager
    async def test_lifespan(_app):
        yield

    previous_lifespan = app.router.lifespan_context
    app.router.lifespan_context = test_lifespan
    app.dependency_overrides[get_db] = override_db
    with testing_session() as db:
        seed_products(db)
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        app.router.lifespan_context = previous_lifespan
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_root_and_health(client):
    assert client.get("/").json()["status"] == "running"
    assert client.get("/health").json() == {"status": "ok"}


def test_product_list_search_filter_and_details(client):
    products = client.get("/api/products")
    assert products.status_code == 200 and len(products.json()) >= 20
    found = client.get("/api/products/search", params={"search": "linen", "category": "Dresses", "max_price": 100})
    assert found.status_code == 200 and found.json()[0]["name"] == "Linen Day Dress"
    product_id = products.json()[0]["id"]
    assert client.get(f"/api/products/{product_id}").status_code == 200
    assert client.get("/api/products/9999").status_code == 404


def test_user_create_retrieve_update_and_missing(client):
    payload = {"name": "Asha Rao", "email": "asha@example.com", "favorite_colors": ["Navy"]}
    created = client.post("/api/users", json=payload)
    assert created.status_code == 201
    user_id = created.json()["id"]
    assert client.get(f"/api/users/{user_id}").json()["favorite_colors"] == ["Navy"]
    updated = client.put(f"/api/users/{user_id}", json={"sizes": ["M", "L"]})
    assert updated.status_code == 200 and updated.json()["sizes"] == ["M", "L"]
    assert client.put("/api/users/9999", json={"sizes": ["M"]}).status_code == 404
    assert client.get("/api/users/9999").status_code == 404
    assert client.post("/api/users", json=payload).status_code == 409


def test_stylist_recommendations_and_validation(client):
    response = client.post("/api/stylist/recommend", json={
        "category": "Dresses", "occasion": "Casual", "colors": ["Sage"],
        "size": "M", "min_budget": 20, "max_budget": 100,
    })
    assert response.status_code == 200
    assert response.json()["recommendations"]
    assert "explanation" in response.json()["recommendations"][0]
    invalid_range = client.post("/api/stylist/recommend", json={"min_budget": 100, "max_budget": 20})
    assert invalid_range.status_code == 422
    assert client.get("/api/products/search", params={"min_price": 20, "max_price": 5}).status_code == 400
    assert client.post("/api/users", json={"name": "Asha", "email": "bad-email"}).status_code == 422
