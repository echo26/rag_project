from pydantic import BaseModel, ConfigDict


class ChatRequest(BaseModel):
    model_config = ConfigDict(strict=True)

    message: str
    use_rag: bool = True


class ChatResponse(BaseModel):
    model_config = ConfigDict(strict=True)

    response: str
