from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    category: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    occasion: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    color: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    sizes: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    in_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
