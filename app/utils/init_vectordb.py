import asyncio
import sys
from pathlib import Path

# add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.vector_search import vector_service
from app.utils import settings, log


async def init_vector_db():

    try:
        await vector_service.initialize()
    except Exception as e:
        log.exception(f"Failed to init: {e}")
        return

    data_dir = Path(settings.DATA_DIR)

    if not data_dir.exists():
        log.error(f"Data directory {data_dir} does not exist")
        return

    jsonl_files = list(data_dir.glob("*.jsonl"))
    log.debug(f"Found {len(jsonl_files)} JSONL files")

    for file in jsonl_files:
        log.debug(f"Loading {file.name}...")
        await vector_service.load_documents_from_jsonl(file)

    total_docs = vector_service.get_document_count()
    log.info(f"Total documents in database: {total_docs}")
    log.info("Initialization complete!")
