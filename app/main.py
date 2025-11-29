from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.utils import settings
from app.api.v1 import router_v1
from app.schemas.models import HealthResponse
from app.services.vector_search import vector_service
from app.utils import log
from app.utils.init_vectordb import init_vector_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""

    log.info("Starting the app.")
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


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Grantbot", "version": settings.APP_VERSION, "docs": "/docs"}


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    try:
        doc_count = vector_service.get_document_count()
        return HealthResponse(
            status="healthy",
            vector_db_initialized=doc_count > 0,
            documents_count=doc_count,
        )
    except Exception as e:
        log.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


app.include_router(router_v1)
