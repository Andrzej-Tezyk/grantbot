## Getting Started

### Setup
1. Create a `.env` file in the project root
2. Add your Gemini API key:
```
   GEMINI_API_KEY=your_key_here
```
   Get a free API key at https://ai.google.dev/

### Running the Application
```bash
uv sync
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Note:** Docker deployment is supported but may take quite long to build due to the `sentence-transformers` package dependencies.

## Testing

Once running, visit the interactive API documentation at `http://localhost:8000/docs`

### Example Request
```json
{
  "company_id": "123",
  "section_type": "compliance",
  "text": "System przetwarza wyłącznie dane niezbędne",
  "language": "pl",
  "max_sources": 5
}
```


## Simplifications/TODO in future
### Infrastructure
- Database containers currently run alongside the application and should be separated into dedicated containers
- Environment variables are managed through `.env` files (development only) and should use a proper key-value store in production

### Configuration
- Configuration uses hardcoded environment variables in `utils/config.py` rather than TOML files with environment-specific settings (dev/prod)

### AI Integration
- Currently uses Gemini API directly instead of frameworks like LangChain or LLMlight, which does not allow use of models of other vendors
- Prompts need expansion and refinement

### Documentation & Testing
- Missing comprehensive docstrings for automated documentation generation
- No unit tests or end-to-end tests implemented


## How it works?
It is a RAG (Retrieval-Augmented Generation) application that generates grant application sections. It uses vector search to find relevant documents and an LLM to produce context-aware text.

### Application flow
1) Initialization (on startup):
    - Initializes ChromaDB and loads documents from JSONL files in the data/ directory
    - Each document is embedded using a multilingual sentence transformer model
    - Documents are stored with metadata: company_id, section_type, language, etc.
    - Initializes SQLite database for request history

2) Generation Request (POST /generate/generate-seciton):
    - Receives: company_id, section_type, input text, optional max_sources
    - Vector Search:
        - Embeds the input text using the same embedding model
        - Searches ChromaDB for similar documents filtered by company_id and section_type
        - Returns top-k most similar documents (default: 5)
    - Text Generation:
        - Builds context from retrieved documents (up to 30,000 characters)
        - Constructs a prompt with section-specific instructions
        - Sends to Gemini API with the context and input text
        - Returns generated section text
    - History Storage:
        - Saves the request to SQLite: input text, generated text, source document IDs, processing time
        - Response: Generated text, source document IDs, request ID, timestamps, processing time

3) History Access:
    - GET /history/{company_id}: Retrieves generation history for a company (optionally filtered by section_type)
    - GET /history/request/{request_id}: Retrieves a specific request by ID


### Data Flow

```
User Request
    ↓
Vector Search (ChromaDB)
    ↓
Retrieve Similar Documents (filtered by company_id & section_type)
    ↓
Build Context from Documents
    ↓
LLM Generation (Gemini API)
    ↓
Save to History (SQLite)
    ↓
Return Generated Text + Sources
```


## Tech Stack

- **Framework**: FastAPI
- **Vector Store**: ChromaDB (for local use)
- **Embeddings**: sentence-transformers (multilingual model)
- **LLM**: OpenAI API / Anthropic Claude / Azure OpenAI
- **Database**: SQLite (history)
- **Validation**: Pydantic
- **Testing**: pytest, httpx
- **Docker**: docker-compose