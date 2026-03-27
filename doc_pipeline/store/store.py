import logging
import os
from typing import Iterator

from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne

from shared_models import Doc

logger = logging.getLogger(__name__)

load_dotenv()

DB_NAME = "rag"
COLLECTION_NAME = "docs"
BATCH_SIZE = 100


def upsert_docs(docs: Iterator[Doc]) -> None:
    with MongoClient(os.environ["MONGODB_URI"]) as client:
        collection = client[DB_NAME][COLLECTION_NAME]
        batch = []
        total = 0
        for doc in docs:
            data = doc.model_dump(by_alias=True)
            update_fields = {
                k: v for k, v in data.items() if k not in ("_id", "created_at")
            }
            batch.append(
                UpdateOne(
                    {"_id": data["_id"]},
                    {
                        "$set": update_fields,
                        "$setOnInsert": {"created_at": data["created_at"]},
                    },
                    upsert=True,
                )
            )
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
