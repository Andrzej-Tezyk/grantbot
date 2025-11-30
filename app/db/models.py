import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, Float, DateTime, JSON

from app.db.database import Base


class RequestHistory(Base):
    __tablename__ = "request_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    request_id = Column(
        String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    company_id = Column(String(100), nullable=False, index=True)
    section_type = Column(String(100), nullable=False)
    input_text = Column(Text, nullable=False)
    generated_text = Column(Text, nullable=False)
    sources = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    processing_time_ms = Column(Float)
