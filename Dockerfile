ARG PYTHON_VERSION=3.12.11
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/
COPY data/ ./data/

# Create directories for persistence
RUN mkdir -p /app/chroma_db

# Expose port
EXPOSE 8000

# Run initialization script and start server
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
