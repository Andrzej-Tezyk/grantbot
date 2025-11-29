from typing import List, Dict, Any
from pathlib import Path

from google import genai
from google.genai import types

from app.utils import settings, log


# TODO: use other providers than google
class TextGeneratorService:
    async def generate_gemini(
        self,
        query: str,
        section_type: str,
        context_documents: List[Dict[str, Any]],  
    ) -> str:
        """ Generate text based on query and context using Gemini model """
        context = self._build_context(context_documents)
        prompt = self._get_system_prompt(section_type)
        log.debug(f"Prompt created: {prompt}")

        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in environment variables")
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

        try:
            response = self.client.models.generate_content(
                model = settings.LLM_MODEL,
                contents = [prompt, context],
                config = types.GenerateContentConfig(
                        temperature = settings.LLM_TEMPERATURE
                    )
            )
            return response.text
        except Exception as e:
            log.error(f"Gemini API error: {e}")
            raise



    def _build_context(self, documents: List[Dict[str, Any]], max_length: int = 30000) -> str:
        """
        Build context string from documents

        Use max_length to control how long context can be. Change depending on model used
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
    

    def _get_system_prompt(self, section_type: str) -> str:
        base_prompt = "You are an expert in writing grant applications and project financing proposals."
        
        path_to_guidelines = Path("app/prompts/gemini_system_prompt.md")
        with open(path_to_guidelines, "r", encoding="utf-8") as f:
            guidelines = f.read()

        section_specific = {
            "market_analysis": "You specialize in market and competition analysis.",
            "innovation_description": "You specialize in describing innovation and uniqueness of solutions.",
            "financial_plan": "You specialize in financial planning and project budgeting.",
            "team_description": "You specialize in presenting the competencies of the project team.",
        }
        addition = section_specific.get(section_type, "")

        return f"{base_prompt} {addition} {guidelines}"

text_generator = TextGeneratorService()