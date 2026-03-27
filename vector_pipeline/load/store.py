import os
from datetime import datetime
from typing import Iterator

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from models import EmbeddedChunk

load_dotenv()

COLLECTION_NAME = "rule_based_recursive"
VECTOR_SIZE = 1024  # bge-m3
BATCH_SIZE = 1000


def _ensure_collection(client: QdrantClient) -> None:
    existing = {c.name for c in client.get_collections().collections}
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )


def _log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def store_chunks(embedded: Iterator[EmbeddedChunk]) -> None:
    # close() releases the underlying httpx session → no fd leak
    client = QdrantClient(url=os.environ["QDRANT_URL"])
    try:
        _ensure_collection(client)

        batch = []
        total = 0
        for chunk in embedded:
            batch.append(
                PointStruct(
                    id=abs(hash(chunk.chunk_id)) % (2**63),
                    vector=chunk.embedding,
                    payload={
                        "chunk_id": chunk.chunk_id,
                        "doc_id": chunk.doc_id,
                        "chunked_text": chunk.chunked_text,
                        "source": chunk.source,
                        "url_path_suffix": chunk.url_path_suffix,
                    },
                )
            )
            if len(batch) == BATCH_SIZE:
                client.upsert(collection_name=COLLECTION_NAME, points=batch)
                total += len(batch)
                _log(f"stored {total} chunks")
                batch.clear()

        if batch:
            client.upsert(collection_name=COLLECTION_NAME, points=batch)
            total += len(batch)
            _log(f"stored {total} chunks")
    finally:
        client.close()
