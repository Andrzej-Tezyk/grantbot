from pydantic_settings import BaseSettings
import os

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # API settings
    APP_NAME: str = "grantbot"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Vector DB settings
    CHROMA_PERSIST_DIR: str = "./app/db/chroma_db"
    COLLECTION_NAME: str = "grant_documents"
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    TOP_K_RESULTS: int = 5

    # LLM settings
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    LLM_MODEL: str = "gemini-2.5-flash"  # gemini-2.0-flash (better free limits)
    LLM_TEMPERATURE: float = 0.5

    # Database settings
    DATABASE_URL: str = ""

    DATA_DIR: str = "./data"

    class Config:
        env_file = ".env"
        case_sensitive = True
