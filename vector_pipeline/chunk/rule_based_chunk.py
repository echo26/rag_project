from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)

# single separator, hard split
char_text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=500,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)

# tries multiple separators in order
recursive_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=200, length_function=len, is_separator_regex=False
)


def _build_chunks(doc: dict, chunks: list[str]) -> list[dict]:
    doc_id = str(doc["_id"])
    title = doc["title"]
    url_path_suffix = f"/wiki/{title.replace(' ', '_')}"
    return [
        {
            "doc_id": doc_id,
            "chunk_id": f"{doc_id}_{i}",
            "chunked_text": chunk,
            "source": title,
            "url_path_suffix": url_path_suffix,
        }
        for i, chunk in enumerate(chunks)
    ]


def rule_based_length_chunk(doc: dict) -> list[dict]:
    chunks = char_text_splitter.split_text(doc["text"])
    return _build_chunks(doc, chunks)


def rule_based_recursive_chunk(doc: dict) -> list[dict]:
    chunks = recursive_text_splitter.split_text(doc["text"])
    return _build_chunks(doc, chunks)
