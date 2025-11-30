from typing import Any
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
        context_documents: list[dict[str, Any]],
    ) -> str:
        """Generate text based on query and context using Gemini model"""
        context = self._build_context(context_documents)
        prompt = self._get_system_prompt(section_type)
        log.debug(f"Prompt created: {prompt}")

        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in environment variables")
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

        try:
            response = self.client.models.generate_content(
                model=settings.LLM_MODEL,
                contents=[prompt, context],
                config=types.GenerateContentConfig(
                    temperature=settings.LLM_TEMPERATURE
                ),
            )
            return response.text
        except Exception as e:
            log.error(f"Gemini API error: {e}")
            raise

    def _build_context(
        self, documents: list[dict[str, Any]], max_length: int = 30000
    ) -> str:
        """
        Build context string from documents

        Use max_length to control how long context can be. Change depending on model used
        """
        context_parts = []
        total_length = 0

        for i, doc in enumerate(documents, 1):
            doc_text = doc["text"]
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
        with open(path_to_guidelines, encoding="utf-8") as f:
            guidelines = f.read()

        # TODO: config file?
        section_specific = {
            "innovation_description": (
                "Write a concise and clear description of the innovation, focusing on the technological ",
                "novelty, use of AI, automation aspects and how the solution improves existing processes.",
            ),
            "market_analysis": "Provide a market analysis describing target customers, market needs, trends, competition and factors driving demand for the solution.",
            "ip_strategy": "Describe the intellectual property strategy, covering ownership of code, licensing of models, data handling rules and protection measures.",
            "compliance": "Explain compliance and data-protection measures, including GDPR/RODO principles, data minimization, security controls and user rights.",
            "deliverables": "Describe the planned project deliverables, including documents, software modules, reports, integrations and final outputs.",
            "budget": "Prepare a structured budget description, outlining cost categories such as personnel, infrastructure, licenses and project operations.",
            "risk_management": "Identify key risks (technical, operational, regulatory) and describe mitigation strategies and monitoring mechanisms.",
            "team": "Describe the project team, highlighting competencies, relevant experience and roles needed to execute the project.",
            "impact": "Explain the expected impact of the project on users, processes or the ecosystem, emphasizing improvements, efficiency and value creation.",
            "environment": "Describe environmental and sustainability aspects, including energy efficiency, green IT practices and reduction of environmental footprint.",
        }
        addition = section_specific.get(section_type, "")

        return f"{base_prompt} {addition} {guidelines}"


text_generator = TextGeneratorService()
