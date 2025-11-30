from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import RequestHistory
from app.schemas.models import HistoryItem
from app.utils import log


class HistoryService:
    @staticmethod
    async def save_request(
        session: AsyncSession,
        request_id: UUID,
        company_id: str,
        section_type: str,
        input_text: str,
        generated_text: str,
        sources: list[str],
        processing_time_ms: float
    ) -> RequestHistory:
        """Save request to history"""
        try:
            history_entry = RequestHistory(
                request_id=request_id,
                company_id=company_id,
                section_type=section_type,
                input_text=input_text,
                generated_text=generated_text,
                sources=sources,
                processing_time_ms=processing_time_ms
            )
            
            session.add(history_entry)
            await session.commit()
            await session.refresh(history_entry)
            
            log.info(f"Saved history entry: {request_id}")
            return history_entry
        except Exception as e:
            await session.rollback()
            log.error(f"Error saving history: {e}")
            raise
    

    @staticmethod
    async def get_company_history(
        session: AsyncSession,
        company_id: str,
        limit: int = 50,
        section_type: str = ""
    ) -> list[HistoryItem]:
        """Get history for a company"""
        try:
            query = select(RequestHistory).where(
                RequestHistory.company_id == company_id
            )
            
            if section_type:
                query = query.where(RequestHistory.section_type == section_type)
            
            query = query.order_by(RequestHistory.created_at.desc()).limit(limit)
            
            result = await session.execute(query)
            entries = result.scalars().all()
            
            return [
                HistoryItem(
                    request_id=entry.request_id,
                    company_id=entry.company_id,
                    section_type=entry.section_type,
                    input_text=entry.input_text,
                    generated_text=entry.generated_text,
                    sources=entry.sources,
                    created_at=entry.created_at,
                    processing_time_ms=entry.processing_time_ms
                )
                for entry in entries
            ]
        except Exception as e:
            log.error(f"Error fetching history: {e}")
            raise
    
    
    @staticmethod
    async def get_request_by_id(
        session: AsyncSession,
        request_id: UUID
    ) -> HistoryItem:
        """Get specific request by ID"""
        try:
            query = select(RequestHistory).where(
                RequestHistory.request_id == request_id
            )
            
            result = await session.execute(query)
            entry = result.scalar_one_or_none()
            
            if not entry:
                return None
            
            return HistoryItem(
                request_id=entry.request_id,
                company_id=entry.company_id,
                section_type=entry.section_type,
                input_text=entry.input_text,
                generated_text=entry.generated_text,
                sources=entry.sources,
                created_at=entry.created_at,
                processing_time_ms=entry.processing_time_ms
            )
        except Exception as e:
            log.error(f"Error fetching request: {e}")
            raise

history = HistoryService()