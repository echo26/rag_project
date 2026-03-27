# RAG Ingest Pipeline

Ingestion pipeline that loads Wikipedia articles from HuggingFace, chunks them, generates embeddings, and stores them in Qdrant.

```bash
cd pipeline
uv sync
```

## Ollama Setup

Install Ollama and pull the required models:

```bash
# Install: https://ollama.com
ollama pull bge-m3
```

Ollama must be running before starting the pipeline:

```bash
ollama serve
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
