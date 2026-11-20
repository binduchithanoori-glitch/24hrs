from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    favorite_colors: Mapped[str] = mapped_column(Text, nullable=False, default="")
    favorite_categories: Mapped[str] = mapped_column(Text, nullable=False, default="")
    sizes: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    style_preferences: Mapped[str] = mapped_column(Text, nullable=False, default="")
