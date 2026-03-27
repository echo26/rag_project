from typing import Iterator

from chunk.rule_based_chunk import rule_based_length_chunk
from models import Chunk, Doc


def chunk_articles(articles: Iterator[Doc]) -> Iterator[Chunk]:
    for doc in articles:
        yield from rule_based_length_chunk(doc)
