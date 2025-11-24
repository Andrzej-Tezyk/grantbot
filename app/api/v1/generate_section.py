import logging
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, APIRouter

from app.schemas.models import GenerateSectionResponse, GenerateSectionRequest
from app.services.vector_search import vector_service
from app.utils.config import settings


log = logging.getLogger("grantbot-api")


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
        generated_text = await text_generator