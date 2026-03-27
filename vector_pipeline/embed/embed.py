from typing import Iterator

from langchain_ollama import OllamaEmbeddings

from models import Chunk, EmbeddedChunk

# 1024 size vector model
embeddings_model = OllamaEmbeddings(model="bge-m3")

# increase to improve embed bottleneck at pipeline
BATCH_SIZE = 128


def embed_chunks(chunks: Iterator[Chunk]) -> Iterator[EmbeddedChunk]:
    batch = []
    for chunk in chunks:
        batch.append(chunk)
        if len(batch) == BATCH_SIZE:
            texts = [c.chunked_text for c in batch]
            embeddings = embeddings_model.embed_documents(texts)
            for c, emb in zip(batch, embeddings):
                yield EmbeddedChunk(**c.model_dump(), embedding=emb)
            batch.clear()
    if batch:
        texts = [c.chunked_text for c in batch]
        embeddings = embeddings_model.embed_documents(texts)
        for c, emb in zip(batch, embeddings):
            yield EmbeddedChunk(**c.model_dump(), embedding=emb)
