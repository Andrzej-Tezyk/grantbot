FOCUS ON POLISH LANGUAGE


## How to run the project?

create .env file in the root and add a variable GEMINI_API_KEY = your_key


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