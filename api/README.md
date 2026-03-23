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

## Test

```bash
uv run pytest
```
