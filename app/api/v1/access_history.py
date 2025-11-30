from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import log
from app.schemas.models import HistoryItem
from app.services.history import HistoryService
from app.db.database import get_session

router_history = APIRouter(prefix="/history")


@router_history.get(
    "/{company_id}",
    response_model=list[HistoryItem],
    tags=["History"]
)
async def get_history(
    company_id: str,
    section_type: str | None = None,
    limit: int = 50,
    session: AsyncSession = Depends(get_session)
):
    """
    Get generation history for a specific company.
    
    Optionally filter by section_type and limit results.
    """
    try:
        log.info(f"Fetching history for company_id={company_id}")
        
        history = await HistoryService.get_company_history(
            session=session,
            company_id=company_id,
            section_type=section_type,
            limit=min(limit, 100)  # Max 100 results
        )
        
        log.info(f"Found {len(history)} history entries")
        return history
        
    except Exception as e:
        log.error(f"Error fetching history: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching history: {str(e)}"
        )

@router_history.get(
    "/request/{request_id}",
    response_model=HistoryItem,
    tags=["History"]
)
async def get_request(
    request_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get specific request by ID"""
    try:
        request_uuid = UUID(request_id)
        
        history_item = await HistoryService.get_request_by_id(
            session=session,
            request_id=request_uuid
        )
        
        if not history_item:
            raise HTTPException(
                status_code=404,
                detail=f"Request {request_id} not found"
            )
        
        return history_item
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error fetching request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))