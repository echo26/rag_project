_SYSTEM = (
    "You are a helpful assistant. Answer the user's question based on the provided context. "
    "If the context doesn't contain relevant information, say so honestly."
)

_RAG_TEMPLATE = """{system}

Context:
{context}

Question: {query}"""

_DIRECT_TEMPLATE = """{system}

Question: {query}"""


def build_prompt(query: str, context: list[str]) -> str:
    if context:
        context_text = "\n\n".join(f"[{i + 1}] {c}" for i, c in enumerate(context))
        return _RAG_TEMPLATE.format(system=_SYSTEM, context=context_text, query=query)
    return _DIRECT_TEMPLATE.format(system=_SYSTEM, query=query)
