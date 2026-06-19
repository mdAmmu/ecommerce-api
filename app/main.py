from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import engine
from app.dependencies.database import get_db
from app.api.auth import router as auth_router
from app.api.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("Database connection successful")

    except Exception as e:
        raise RuntimeError(
            f"Database connection failed: {e}"
        )

    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for the ecommerce platform",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(auth_router)
app.include_router(users_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    return {"message": "database connected"}