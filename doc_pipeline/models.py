from pydantic import BaseModel


class RawArticle(BaseModel):
    id: str
    title: str
    text: str
