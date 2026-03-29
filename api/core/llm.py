from collections.abc import AsyncIterator

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

import config


def _get_llm() -> ChatAnthropic:
    return ChatAnthropic(  # type: ignore[call-arg]
        model=config.LLM_MODEL,
        api_key=config.ANTHROPIC_API_KEY,
    )


async def stream_response(message: str) -> AsyncIterator[str]:
    llm = _get_llm()
    async for chunk in llm.astream([HumanMessage(content=message)]):
        if chunk.content:
            yield str(chunk.content)
