
## Simplifications/TODO in future
- Databases are run from the same container that app itself. Should be put into their own containers
- Class with hardcoded env variables in utils/config.py to then pass them as settings.VARIABLE, fast solution for small project. Should implement with toml files instead with division between prod/dev.
- Use of .env is only for dev. Should be Key-value storage instead
- Use of gemini API instead of Lanchain or LLMlight to be able to use models of other vendors 


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