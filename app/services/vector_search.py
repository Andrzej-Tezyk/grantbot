import logging
from pathlib import Path
import json
import csv
from typing import List, Dict, Any

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
        self.collection = None # created in def initizlize


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


    async def load_documents_from_csv(self, filepath: Path):
        """ Load documents from CSV file """
        documents = []
        metadatas = []
        ids = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                documents.append(row['text'])
                metadatas.append({
                    'company_id': row['company_id'],
                    'section_type': row['section_type'],
                    'language': row.get('language', 'pl'),
                    'source_type': row.get('source_type', ''),
                    'created_at': row.get('created_at', '')
                })
                ids.append(row['id'])
        
        if documents:
            embeddings = self.embedding_model.encode(documents, show_progress_bar=True)
            self.collection.add(
                embeddings=embeddings.tolist(),
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            log.info(f"Loaded {len(documents)} documents from {filepath}")


    async def search(
        self,
        query: str,
        company_id: str,
        section_type: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for similar documents with filtering"""
        query_embedding = self.embedding_model.encode([query])[0]
        
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k * 3,  # more results to filter
            where={ # filter by metadata
                "$and": [
                    {"company_id": {"$eq": company_id}},
                    {"section_type": {"$eq": section_type}}
                ]
            }
        )
        
        formatted_results = []
        if results['ids'] and results['ids'][0]:
            for i, doc_id in enumerate(results['ids'][0][:top_k]):
                formatted_results.append({
                    'id': doc_id,
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if results['distances'] else None
                })

        return formatted_results


    def get_document_count(self) -> int:
        """ Get total number of documents in collection """
        return self.collection.count() if self.collection else 0


vector_service = VectorSearchService()