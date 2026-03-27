import os
from typing import Iterator

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

DB_NAME = "rag"
COLLECTION_NAME = "docs"
BATCH_SIZE = 100


def extract_docs() -> Iterator[dict]:
    with MongoClient(os.environ["MONGODB_URI"]) as client:
        collection = client[DB_NAME][COLLECTION_NAME]
        cursor = collection.find({}, batch_size=BATCH_SIZE)
        yield from cursor


# AVOID
# all at once -> memory spike
# one by one -> RTT overhead
# pagination -> cursor better

# parallel ranges -> split id range into buckets
# mongoexport -> direcy binary
