## Tech Stack

- **Framework**: FastAPI
- **Vector Store**: ChromaDB (for local use)
- **Embeddings**: sentence-transformers (multilingual model)
- **LLM**: OpenAI API / Anthropic Claude / Azure OpenAI
- **Database**: SQLite (history)
- **Validation**: Pydantic
- **Testing**: pytest, httpx
- **Docker**: docker-compose

## Architecture

```
┌─────────────────┐
│   FastAPI App   │
│   (REST API)    │
└────────┬────────┘
         │
    ┌────┴────────────────────┐
    │                         │
┌───▼────────┐      ┌────────▼─────┐
│  Vector    │      │   History    │
│  Search    │      │   Storage    │
│ (ChromaDB) │      │  (SQLite)    │
└───┬────────┘      └──────────────┘
    │
┌───▼────────┐
│ Embeddings │
│  Model     │
└────────────┘
```