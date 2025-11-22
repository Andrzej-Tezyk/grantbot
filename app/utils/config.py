from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API settings
    APP_NAME: str = "grantbot"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Vector DB settings
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    COLLECTION_NAME: str = "grant_documents"
    EMBEDDING_MODEL: str = ""
    TOP_K_RESULTS: int = 5

    # LLM settings
    LLM_PROVIDER: str = "google"
    GEMINI_API_KEY: Optional[str] = None
    LLM_MODEL: str = ""
    LLM_TEMPERATURE: float = 0.7

    # Database settings
    DATABASE_URL: str = ""

    DATA_DIR: str = "./data"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
