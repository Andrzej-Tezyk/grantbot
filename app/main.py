from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.logging import get_custom_logger
from app.utils import settings
from app.api.v1 import router_v1


log = get_custom_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""

    log.info("Starting the app.")
    # init databases

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


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Grantbot", "version": settings.APP_VERSION, "docs": "/docs"}


app.include_router(router_v1)
