from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import get_settings
from app.db.database import Base, SessionLocal, engine, seed_products
from app import models  # noqa: F401 - register all SQLAlchemy models

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_products(db)
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", debug=settings.debug, lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_credentials=True,
                   allow_methods=["GET", "POST", "PUT", "OPTIONS"], allow_headers=["*"])
app.include_router(router)
