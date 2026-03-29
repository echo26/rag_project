from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class RawArticle(BaseModel):
    id: str
    title: str
    text: str

    @field_validator("id", mode="before")
    @classmethod
    def coerce_id_to_str(cls, v: object) -> str:
        return str(v)


class Doc(BaseModel):
    id: str = Field(alias="_id")
    source: str
    doc_id: str
    title: str
    text: str
    url_path_suffix: str
    created_at: datetime
    updated_at: datetime

    model_config = {"populate_by_name": True}
