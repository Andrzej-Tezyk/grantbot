from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils import settings
from app.api.v1 import router_v1
from app.utils import log
from app.db.init_vectordb import init_vector_db
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""

    log.info("Starting the app.")
    await init_db()
    await init_vector_db()
    log.info("Vector service initialized.")

    log.info("App started successfully.")

    yield

    log.info("Shutting down.")


app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


app.include_router(router_v1)
