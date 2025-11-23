from contextlib import asynccontextmanager
from uuid import uuid4
from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.logging import get_custom_logger
from app.utils.config import settings


log = get_custom_logger("grantbot")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Startup and shutdown events """

    log.info("Starting the app.")
    # init databases

    log.info("App started successfully.")

    yield

    log.info("Shutting down.")

app = FastAPI(title=settings.APP_NAME,
              version=settings.APP_VERSION,
              lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Grantbot",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


# app.include_router(prefix = "/api/v1/generate_seciton")
