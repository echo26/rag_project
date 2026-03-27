import json
import logging
from typing import Iterator

from models import RawArticle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

JSONL_FILE = "simplewiki.jsonl"


def load_articles() -> Iterator[RawArticle]:
    with open(JSONL_FILE, encoding="utf-8") as f:
        for line in f:
            yield RawArticle.model_validate(json.loads(line))
