import logging
from pathlib import Path
import json

import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer

from app.utils.config import settings


log = logging.getLogger("grantbot-api")


class VectorSearchService:
    def __init__(self):
        self.client = chromadb.Client(
            ChromaSettings(
                persist_directory=settings.CHROMA_PERSIST_DIR,
                anonymized_telemetry=False,
            )
        )
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.collection = None

    async def initialize(self):
        """Initialize or get existing collection"""
        try:
            self.collection = self.client.get_or_create_collection(
                name=settings.COLLECTION_NAME
            )
            log.info(f"Collection initialized with {self.collection.count()} documents")
        except Exception as e:
            log.error(f"Error initlizing collection: {e}")
            raise

    async def load_documents_from_jsonl(self, filepath: Path):
        """Load documents from JSONL file"""

        documents = []
        metadatas = []
        ids = []

        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                doc = json.loads(line.strip())
                documents.append(doc["text"])
                metadatas.append(
                    {
                        "company_id": doc["company_id"],
                        "section_type": doc["section_type"],
                        "language": doc.get("language", "pl"),
                        "source_type": doc.get("source_type", ""),
                        "created_at": doc.get("created_at", ""),
                    }
                )

        if documents:
            embeddings = self.embedding_model.encode(documents, show_progress_bar=True)

            self.collection.add(
                embeddings=embeddings.tolist(),
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            log.info(f"Loaded {len(documents)} documents from {filepath}")