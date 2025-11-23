import logging
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.models import GenerateSectionResponse, GenerateSectionRequest

log = logging.getLogger("grantbot-api")

@app.post(
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
        

    
