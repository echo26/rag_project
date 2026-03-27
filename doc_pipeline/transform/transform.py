import re
from datetime import datetime, timezone
from typing import Iterator
from urllib.parse import quote

from models import RawArticle
from shared_models import Doc

INGESTED_AT = datetime.now(timezone.utc)


_SKIP_PREFIXES = (
    "thumb|",
    "thumbnail|",  # image captions
    "alt=",  # image alt text
    "right|",
    "left|",
    "center|",  # float image markup
    "File:",
    "Image:",  # file references
    "!",
    "|-",
    "|}",  # table header/row/end
    "|",  # table data / any remaining pipe lines
)

_TABLE_ROW_RE = re.compile(r"^[\d\s]+(\|\|.+){2,}$")


def _skip_line(line: str) -> bool:
    if re.match(r"^\d+px\|", line):
        return True
    if _TABLE_ROW_RE.match(line):
        return True
    return False


def parse_text(text: str) -> str:
    paragraphs = []
    current = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        if line.startswith(_SKIP_PREFIXES) or _skip_line(line):
            continue
        current.append(line)
    if current:
        paragraphs.append(" ".join(current))
    text = "\n\n".join(paragraphs)
    text = text.translate(str.maketrans("", "", "\"'|"))
    return re.sub(r" {2,}", " ", text).strip()


def transform_articles(articles: Iterator[RawArticle]) -> Iterator[Doc]:
    for article in articles:
        yield transform_article(article)


def transform_article(article: RawArticle) -> Doc:
    return Doc.model_validate(
        {
            "_id": f"simplewiki_{article.id}",
            "source": "simplewiki",
            "doc_id": article.id,
            "title": article.title,
            "text": parse_text(article.text),
            "url_path_suffix": quote(article.title.replace(" ", "_")),
            "created_at": INGESTED_AT,
            "updated_at": INGESTED_AT,
        }
    )
