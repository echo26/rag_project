from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)

from models import Chunk, Doc

# single separator, hard split
char_text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)

# tries multiple separators in order (built in)
recursive_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=200, length_function=len, is_separator_regex=False
)


def _build_chunks(doc: Doc, chunks: list[str]) -> list[Chunk]:
    return [
        Chunk(
            doc_id=doc.id,
            chunk_id=f"{doc.id}_{i}",
            chunked_text=chunk,
            source=doc.title,
            url_path_suffix=doc.url_path_suffix,
        )
        for i, chunk in enumerate(chunks)
    ]


# limited when paragraph size is over the chunk size
# can't chunk properly with single separator
def rule_based_length_chunk(doc: Doc) -> list[Chunk]:
    chunks = char_text_splitter.split_text(doc.text)
    return _build_chunks(doc, chunks)


# use recursive to handle chunk boundary problem
def rule_based_recursive_chunk(doc: Doc) -> list[Chunk]:
    chunks = recursive_text_splitter.split_text(doc.text)
    return _build_chunks(doc, chunks)
