from collections.abc import AsyncIterator
from typing import cast

from core.llm import stream_response
from core.utils import build_prompt
from graph.rag_graph import rag_graph
from graph.state import RAGState


async def stream_rag_response(query: str, use_rag: bool = True) -> AsyncIterator[str]:
    if use_rag:
        state = cast(RAGState, await rag_graph.ainvoke({"query": query, "context": []}))
        prompt = build_prompt(state["query"], state["context"])
    else:
        prompt = build_prompt(query, [])
    async for chunk in stream_response(prompt):
        yield chunk
