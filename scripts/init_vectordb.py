import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.vector_search import vector_service
from app.utils.config import settings

async def main():
    print("Initializing vector database...")
    
    # Initialize service
    await vector_service.initialize()
    
    # Load documents from data directory
    data_dir = Path(settings.DATA_DIR)
    
    if not data_dir.exists():
        print(f"Error: Data directory {data_dir} does not exist")
        return
    
    # Load JSONL files
    jsonl_files = list(data_dir.glob("*.jsonl"))
    print(f"Found {len(jsonl_files)} JSONL files")
    
    for file in jsonl_files:
        print(f"Loading {file.name}...")
        await vector_service.load_documents_from_jsonl(file)
    
    # Load CSV files
    csv_files = list(data_dir.glob("*.csv"))
    print(f"Found {len(csv_files)} CSV files")
    
    for file in csv_files:
        print(f"Loading {file.name}...")
        await vector_service.load_documents_from_csv(file)
    
    total_docs = vector_service.get_document_count()
    print(f"\\nTotal documents in database: {total_docs}")
    print("Initialization complete!")

if __name__ == "__main__":
    asyncio.run(main())