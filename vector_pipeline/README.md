# RAG Ingest Pipeline

Ingestion pipeline that loads Wikipedia articles from HuggingFace, chunks them, generates embeddings, and stores them in Qdrant.

```bash
cd pipeline
uv sync
```

## Run

```bash
# Default: ingest 100,000 articles
uv run python main.py
```

## Test

```bash
uv run pytest
```
