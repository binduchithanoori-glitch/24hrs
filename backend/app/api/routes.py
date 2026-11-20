from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.shopping import (
    ProductResponse, Recommendation, ShoppingRequest, ShoppingResponse,
    UserCreate, UserResponse, UserUpdate,
)
from app.services.stylist import explain_recommendation, recommend_products

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Welcome to LookLoom AI API", "status": "running", "docs": "/docs"}


@router.get("/health")
def health():
    return {"status": "ok"}


def _product_query(db, search, category, color, size, min_price, max_price):
    query = db.query(Product)
    if search:
        term = f"%{search.strip()}%"
        query = query.filter(or_(Product.name.ilike(term), Product.description.ilike(term)))
    if category:
        query = query.filter(func.lower(Product.category) == category.casefold())
    if color:
        query = query.filter(Product.color.ilike(f"%{color.strip()}%"))
    if size:
        query = query.filter(Product.sizes.ilike(f"%{size.strip()}%"))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    return query


def _check_price_range(min_price, max_price):
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(status_code=400, detail="min_price must not exceed max_price")


@router.get("/api/products/search", response_model=list[ProductResponse])
def search_products(search: str | None = Query(None, max_length=100), category: str | None = Query(None, max_length=60),
                    color: str | None = Query(None, max_length=120), size: str | None = Query(None, max_length=20),
                    min_price: float | None = Query(None, ge=0), max_price: float | None = Query(None, ge=0),
                    db: Session = Depends(get_db)):
    _check_price_range(min_price, max_price)
    products = _product_query(db, search, category, color, size, min_price, max_price).order_by(Product.id).all()
    return [ProductResponse.from_product(product) for product in products]


@router.get("/api/products", response_model=list[ProductResponse])
def list_products(limit: int = Query(100, ge=1, le=200), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    products = db.query(Product).order_by(Product.id).offset(offset).limit(limit).all()
    return [ProductResponse.from_product(product) for product in products]


@router.get("/api/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse.from_product(product)


@router.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = User(name=user_data.name.strip(), email=str(user_data.email).lower(),
                favorite_colors=",".join(user_data.favorite_colors),
                favorite_categories=",".join(user_data.favorite_categories), sizes=",".join(user_data.sizes),
                style_preferences=user_data.style_preferences)
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A user with this email already exists")
    return UserResponse.from_user(user)


@router.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_user(user)


@router.put("/api/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, changes: UserUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for field in ("name", "style_preferences"):
        value = getattr(changes, field)
        if value is not None:
            setattr(user, field, value.strip() if field == "name" else value)
    for field in ("favorite_colors", "favorite_categories", "sizes"):
        value = getattr(changes, field)
        if value is not None:
            setattr(user, field, ",".join(value))
    db.commit()
    db.refresh(user)
    return UserResponse.from_user(user)


@router.post("/api/stylist/recommend", response_model=ShoppingResponse)
def get_recommendations(preferences: ShoppingRequest, db: Session = Depends(get_db)):
    ranked = recommend_products(db, preferences)
    results = [Recommendation(product=ProductResponse.from_product(product), score=score,
                               explanation=explain_recommendation(product, preferences, score))
               for score, product in ranked]
    return ShoppingResponse(preferences=preferences, recommendations=results)
