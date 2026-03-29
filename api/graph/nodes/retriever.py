from langchain_openai import OpenAIEmbeddings
from pydantic import SecretStr

import config
from graph.state import RAGState
from vectordb.qdrant import similarity_search  # pylint: disable=no-name-in-module

_embeddings = OpenAIEmbeddings(
    model=config.EMBEDDING_MODEL,
    dimensions=config.EMBEDDING_DIMENSIONS,
    api_key=SecretStr(config.OPENAI_API_KEY),
)


async def retrieve(state: RAGState) -> dict:
    embedding = await _embeddings.aembed_query(state["query"])
    results = await similarity_search(embedding)
    context = [
        r.payload["chunked_text"] for r in results if r.payload and r.payload.get("chunked_text")
    ]
    return {"context": context}
