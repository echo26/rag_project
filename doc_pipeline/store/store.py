import logging
import os
from typing import Iterator
from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne

logger = logging.getLogger(__name__)


load_dotenv()

DB_NAME = "rag"
COLLECTION_NAME = "docs"
BATCH_SIZE = 100


def upsert_docs(docs: Iterator[dict]) -> None:
    # MongoClient as context manager: closes connection on exit → no fd leak
    with MongoClient(os.environ["MONGODB_URI"]) as client:
        collection = client[DB_NAME][COLLECTION_NAME]
        batch = []
        total = 0
        for doc in docs:
            update_fields = {
                k: v for k, v in doc.items() if k not in ("_id", "created_at")
            }
            # UpdateOne with upsert: insert if not exists,
            # update if exists → safe to re-run
            batch.append(
                UpdateOne(
                    {"_id": doc["_id"]},
                    {
                        "$set": update_fields,
                        "$setOnInsert": {"created_at": doc["created_at"]},
                    },
                    upsert=True,
                )
            )
            # batch: send N ops in one network round-trip
            # instead of N round-trips
            if len(batch) == BATCH_SIZE:
                result = collection.bulk_write(batch, ordered=False)
                total += len(batch)
                logger.info(
                    "upserted %d docs (total: %d) — matched=%d upserted=%d",
                    len(batch),
                    total,
                    result.matched_count,
                    result.upserted_count,
                )
                batch.clear()
        if batch:
            result = collection.bulk_write(batch, ordered=False)
            total += len(batch)
            logger.info(
                "upserted %d docs (total: %d) — matched=%d upserted=%d",
                len(batch),
                total,
                result.matched_count,
                result.upserted_count,
            )
