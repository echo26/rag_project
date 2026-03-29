from pydantic import BaseModel, ConfigDict


class ChatRequest(BaseModel):
    model_config = ConfigDict(strict=True)

    message: str


class ChatResponse(BaseModel):
    model_config = ConfigDict(strict=True)

    response: str
