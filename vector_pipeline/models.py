from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field


class Doc(BaseModel):
    id: str = Field(alias="_id")
    source: str
    doc_id: Annotated[str, BeforeValidator(str)]
    title: str
    text: str
    url_path_suffix: str
    created_at: datetime
    updated_at: datetime

    model_config = {"populate_by_name": True}


class Chunk(BaseModel):
    doc_id: str
    chunk_id: str
    chunked_text: str
    source: str
    url_path_suffix: str


class EmbeddedChunk(Chunk):
    embedding: list[float]
