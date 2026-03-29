import anthropic
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from core.llm import stream_response
from models import ChatRequest

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="message must not be empty")

    async def generate():
        try:
            async for chunk in stream_response(request.message):
                yield chunk
        except anthropic.APIError as e:
            yield f"\n[error: {e}]"

    return StreamingResponse(generate(), media_type="text/plain")
