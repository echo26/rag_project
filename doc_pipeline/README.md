# Docs Pipeline

Pipeline that scrapes source data, transforms it into structured documentation, adds metadata, and upserts it to MongoDB.

## Stages

1. **scrape** — fetch raw articles from source
2. **transform** — convert raw data to documentation format
3. **metadata** — enrich documents with metadata
4. **store** — upsert documents to MongoDB

## Setup

```bash
cd docs_pipeline
uv sync
```

## Run

```bash
uv run python main.py
```

## Test

```bash
uv run pytest
```
