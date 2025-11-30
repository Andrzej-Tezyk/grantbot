ARG PYTHON_VERSION=3.12-slim
FROM python:${PYTHON_VERSION} AS base

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies required by chromadb / sentence-transformers
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       curl \
       git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
RUN chmod +x /usr/local/bin/uv

# Install Python dependencies using uv (respects uv.lock automatically)
COPY pyproject.toml ./pyproject.toml
COPY uv.lock ./uv.lock
RUN uv sync --frozen --no-dev

# Copy application source and assets
COPY app ./app
COPY data ./data

# Prepare runtime directories and user
RUN mkdir -p /app/chroma_db \
    && useradd --create-home --shell /bin/bash grantbot \
    && chown -R grantbot:grantbot /app

USER grantbot

ENV CHROMA_PERSIST_DIR=/app/chroma_db \
    DATA_DIR=/app/data

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
