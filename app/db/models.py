from sqlalchemy import Column, String, Text, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone
from app.db.database import Base


class RequestHistory(Base):
    __tablename__ = "request_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(
        UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4
    )
    company_id = Column(String(100), nullable=False, index=True)
    section_type = Column(String(100), nullable=False)
    input_text = Column(Text, nullable=False)
    generated_text = Column(Text, nullable=False)
    sources = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)
    processing_time_ms = Column(Float)
