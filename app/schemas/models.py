from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4


class HealthResponse(BaseModel):
    status: str
    vector_db_initialized: bool
    documents_count: int


class GenerateSectionRequest(BaseModel):
    company_id: str = Field(description="Company identifier")
    section_type: str = Field(description="Type of section to generate")
    text: str = Field(min_length=10, description="Input text for context search")
    language: Optional[str] = Field("pl", description="Language code")
    max_sources: Optional[int] = Field(5, ge=1, le=20)  # between 1 and 20


class GenerateSectionResponse(BaseModel):
    company_id: str
    section_type: str
    generated_text: str
    sources: List[str]
    request_id: UUID
    created_at: datetime
    processing_time_ms: float


class HistoryItem(BaseModel):
    request_id: UUID
    company_id: str
    section_type: str
    input_text: str
    generated_text: str
    sources: List[str]
    created_at: datetime
    processing_time_ms: float
