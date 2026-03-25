import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

JSONL_FILE = "simplewiki.jsonl"


def load_articles():
    with open(JSONL_FILE, encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)
