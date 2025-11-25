from typing import List, Dict, Any
from app.utils import settings
import logging


log = logging.getLogger(__name__)

# TODO: use other providers than google
class TextGeneratorService:
    async def generate(
        self,
        query: str,
        section_type: str,
        context_documents: List[Dict[str, Any]],
        language: str = "pl"
    ):
        """ Generate text based on query and context """
        pass

    async def generate_gemini(
        self,
        query: str,
        section_type: str,
        context_documents: List[Dict[str, Any]],
        language: str    
    ) -> str:
        """ Generate text based on query and context using Gemini model """
        context = self._build_context(context_documents)


    def _build_context(self, documents: List[Dict[str, Any]], max_length: int = 30000) -> str:
        """
        Build context string from documents

        Use max_length to control how long context can be. Depends on model used
        """
        context_parts = []
        total_length = 0
        
        for i, doc in enumerate(documents, 1):
            doc_text = doc['text']
            if total_length + len(doc_text) > max_length:
                # Truncate if too long
                remaining = max_length - total_length
                doc_text = doc_text[:remaining] + "..."
            
            context_parts.append(f"[Dokument {i} - ID: {doc['id']}]\n{doc_text}\n")
            total_length += len(doc_text)
            
            if total_length >= max_length:
                break
        
        return "\n---\n".join(context_parts)