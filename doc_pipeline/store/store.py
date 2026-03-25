from typing import Iterator


def upsert_docs(docs: Iterator[dict]) -> None:
    for doc in docs:
        print("UPSERT:", doc["title"])  # debug
