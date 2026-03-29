from qdrant_client import AsyncQdrantClient
from qdrant_client.models import ScoredPoint

import config

vector_search_client = AsyncQdrantClient(url=config.QDRANT_URL)


async def similarity_search(embedding: list[float]) -> list[ScoredPoint]:
    result = await vector_search_client.query_points(
        collection_name=config.QDRANT_COLLECTION,
        query=embedding,
        limit=config.RETRIEVER_TOP_K,
        with_payload=True,
    )
    return result.points
