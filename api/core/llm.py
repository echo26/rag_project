from collections.abc import AsyncIterator

import anthropic
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

import config

_RETRYABLE = (anthropic.APIConnectionError, anthropic.RateLimitError)


def _get_llm() -> ChatAnthropic:
    return ChatAnthropic(  # type: ignore[call-arg]
        model=config.LLM_MODEL,
        api_key=config.ANTHROPIC_API_KEY,
        max_retries=0,  # retries handled below
        timeout=config.LLM_TIMEOUT,
    )


async def stream_response(message: str) -> AsyncIterator[str]:
    llm = _get_llm()
    async for attempt in AsyncRetrying(
        retry=retry_if_exception_type(_RETRYABLE),
        stop=stop_after_attempt(config.LLM_MAX_RETRIES + 1),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        reraise=True,
    ):
        with attempt:
            async for chunk in llm.astream([HumanMessage(content=message)]):
                if chunk.content:
                    yield str(chunk.content)
