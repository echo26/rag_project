import os
import time
from typing import Iterator

# from langchain_ollama import OllamaEmbeddings

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from openai import RateLimitError
from pydantic import SecretStr

from models import Chunk, EmbeddedChunk

load_dotenv()

# 1024 size vector model
# embeddings_model = OllamaEmbeddings(model="bge-m3")
# BATCH_SIZE = 128

# truncated to 1024 — compatible with existing bge-m3 collection
embeddings_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=1024,
    api_key=SecretStr(os.environ["OPENAI_API_KEY"]),
)

BATCH_SIZE = 512


def _embed_with_retry(texts: list[str]) -> list[list[float]]:
    for attempt in range(5):
        try:
            return embeddings_model.embed_documents(texts)
        except RateLimitError:
            time.sleep(2**attempt)
    return embeddings_model.embed_documents(texts)


def embed_chunks(chunks: Iterator[Chunk]) -> Iterator[EmbeddedChunk]:
    batch = []
    for chunk in chunks:
        batch.append(chunk)
        if len(batch) == BATCH_SIZE:
            texts = [c.chunked_text for c in batch]
            embeddings = _embed_with_retry(texts)
            for c, emb in zip(batch, embeddings):
                yield EmbeddedChunk(
                    doc_id=c.doc_id,
                    chunk_id=c.chunk_id,
                    chunked_text=c.chunked_text,
                    source=c.source,
                    url_path_suffix=c.url_path_suffix,
                    embedding=emb,
                )
            batch.clear()
    if batch:
        texts = [c.chunked_text for c in batch]
        embeddings = _embed_with_retry(texts)
        for c, emb in zip(batch, embeddings):
            yield EmbeddedChunk(
                doc_id=c.doc_id,
                chunk_id=c.chunk_id,
                chunked_text=c.chunked_text,
                source=c.source,
                url_path_suffix=c.url_path_suffix,
                embedding=emb,
            )
