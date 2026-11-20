import json
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


_settings = get_settings()
_connect_args = {"check_same_thread": False} if _settings.database_url.startswith("sqlite") else {}
engine = create_engine(_settings.database_url, connect_args=_connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_products(db: Session) -> None:
    from app.models.product import Product

    if db.query(Product).first() is not None:
        return
    seed_file = Path(__file__).resolve().parents[2] / "seed" / "products.json"
    with seed_file.open(encoding="utf-8") as file:
        products = json.load(file)
    db.add_all(Product(**item) for item in products)
    db.commit()
