from uuid import uuid4
import time
import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, APIRouter

from app.schemas.models import GenerateSectionResponse, GenerateSectionRequest
from app.services.vector_search import vector_service
from app.services.text_generator import text_generator
from app.utils import settings
from app.utils import log


router_generate_secion = APIRouter(prefix="/generate")


@router_generate_secion.post(
    "/generate-seciton",
    response_model = GenerateSectionResponse,
    tags = ["Generation"]
)
async def generate_section(request: GenerateSectionRequest):
    """
    Generate a section of grant application based on input text.

    Uses RAG to find similar documents and generate relevant content for
    the specified section.
    """
    start_time = time.time()
    request_id = uuid4()

    try:
        log.info(f"Request {request_id}: company={request.company_id}")

        # search for similar documents
        log.debug("Starting vector search ...")
        similar_docs = await vector_service.search(
            query = request.text,
            company_id = request.company_id,
            section_type = request.section_type,
            top_k = request.max_sources or settings.TOP_K_RESULTS
        )

        if not similar_docs:
            raise HTTPException(
                status_code=404,
                detail=f"No documents found for company_id={request.company_id} "
                       f"and section_type={request.section_type}"
            )

        log.info(f"Found {len(similar_docs)} similar documents")

        # generate text
        log.debug(f"Starting text generation ...")
        generated_text = await text_generator.generate_gemini(
            query = request.text,
            section_type = request.section_type,
            context_documents = similar_docs
        )

        # +++++++++++++++++++++++++
        # if generated_text empty

        source_ids = [doc['id'] for doc in similar_docs]

        processing_time_ms = (time.time() - start_time) * 1000

        # save to history
        # await HistoryService.

        log.info(
            f"Request {request_id} completed in {processing_time_ms:.2f}ms"
        )

        return GenerateSectionResponse(
            company_id=request.company_id,
            section_type=request.section_type,
            generated_text=generated_text,
            sources=source_ids,
            request_id=request_id,
            created_at=datetime.utcnow(),
            processing_time_ms=processing_time_ms
        )
    
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error processing request {request_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )