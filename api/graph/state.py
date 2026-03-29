from typing import TypedDict


class RAGState(TypedDict):
    query: str
    context: list[str]
