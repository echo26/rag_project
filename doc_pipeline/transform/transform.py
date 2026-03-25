from typing import Iterator


def transform_articles(articles: Iterator[dict]) -> Iterator[dict]:
    for article in articles:
        yield transform_article(article)


def transform_article(article):
    return article
