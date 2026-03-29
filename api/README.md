# RAG API

FastAPI service for querying the RAG system. Accepts natural language questions and returns answers using a vector database and LLM.

## Setup

```bash
cd api
uv sync
```

Required environment variables in .env

```
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
```

## Run

```bash
uv run fastapi dev app.py
```

The server starts at `http://localhost:8000`.

## Docker

Build and run the API:

```bash
docker build -t fastapi .
docker run -p 8000:8000 --env-file .env -e QDRANT_URL=http://host.docker.internal:6333 fastapi
```

## Test

```bash
uv run pytest
```
