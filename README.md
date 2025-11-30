FOCUS ON POLISH LANGUAGE

prompt content depends on task type



{
  "company_id": "123",
  "section_type": "market_analysis",
  "text": "dotacyjnego w Polsce rośnie, a kluczową grupą docelową są agencje i firmy pozyskujące",
  "language": "pl",
  "max_sources": 5
}



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