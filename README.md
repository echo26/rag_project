# RAG Platform — Wikipedia Q&A

A retrieval-augmented generation (RAG) system built on Wikipedia English, designed for accurate, cited answers over ~6M articles.

## Overview

| Field       | Detail                                                        |
| ----------- | ------------------------------------------------------------- |
| Data source | Wikipedia English dump via HuggingFace (~20 GB, ~6M articles) |
| Stack       | Python, LangChain, LangGraph, FastAPI, Qdrant                 |

## Architecture

```
[Wikipedia HuggingFace dataset]
        │
        ▼
  [Ingest Pipeline]
  - Chunk articles
  - Embed chunks
  - Store in Qdrant
        │
        ▼
  [FastAPI Query API]
  - POST /query → embed query → Qdrant top-5 → stream LLM
  - LLM: Claude via LangChain (SSE streaming)
  - Response: answer text + sources [{title, url}]
```

### Setup

```bash
# Install root dev dependencies (black, pylint, pre-commit, pytest)
uv sync --group dev

# Install git hooks
pre-commit install
```

## Local Setup

Three Docker containers via `docker-compose`:

| Service   | Detail                                                      |
| --------- | ----------------------------------------------------------- |
| `qdrant`  | `qdrant/qdrant:latest` on port 6333, volume `./qdrant_data` |
| `fastapi` | App image on port 8000, reads `.env` for API keys           |
| `ingest`  | Same app image, runs `python ingest.py` once then exits     |

```bash
# Copy and fill in API keys
cp .env.example .env

# Start Qdrant + FastAPI
docker-compose up

# Run ingestion
docker-compose run ingest
```

## Code Quality

### Tools

| Tool         | Purpose            | Config                                                     |
| ------------ | ------------------ | ---------------------------------------------------------- |
| `black`      | Code formatter     | `[tool.black]` in `pyproject.toml` (line-length 88, py313) |
| `pylint`     | Linter             | `[tool.pylint.*]` in each `pyproject.toml`                 |
| `pre-commit` | Git hook runner    | `.pre-commit-config.yaml`                                  |
| `pytest`     | Test runner        | `[tool.pytest.ini_options]` in each `pyproject.toml`       |
| `pytest-cov` | Coverage reporting | via `pytest --cov`                                         |
