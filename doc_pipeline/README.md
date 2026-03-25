# Docs Pipeline

Pipeline that loads Wikipedia articles from a JSONL dump, transforms them into structured documentation, and upserts to MongoDB.

## Stages

1. **scrape** — load raw articles from JSONL dump
2. **transform** — convert raw data to documentation format
3. **metadata** — enrich documents with metadata
4. **store** — upsert documents to MongoDB

## Setup

```bash
cd doc_pipeline
uv sync
```

## Download Wikipedia Dump

1. Download the bz2 dump:

```bash
wget https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-pages-articles.xml.bz2
```

2. Extract:

```bash
bunzip2 simplewiki-latest-pages-articles.xml.bz2
```

3. Convert XML to JSONL (outputs `simplewiki.jsonl`):

```bash
uv run python xml2json.py
```

## Run

```bash
uv run python main.py
```

## Test

```bash
uv run pytest
```
