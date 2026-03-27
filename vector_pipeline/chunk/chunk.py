from chunk.rule_based_chunk import (
    rule_based_length_chunk,
)


def chunk_articles(articles):
    for doc in articles:
        chunks = rule_based_length_chunk(doc)
        # emit chunk individually
        yield from chunks
    pass
