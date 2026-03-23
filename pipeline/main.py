from scrape.scrape import load_articles
from chunk.chunk import chunk_articles
from embed.embed import embed_chunks
from load.store import store_chunks


def main():
    print("[1/4] Loading articles...")
    articles = load_articles()

    print("[2/4] Chunking articles...")
    chunks = chunk_articles(articles)

    print("[3/4] Embedding chunks...")
    embedded = embed_chunks(chunks)

    print("[4/4] Storing in Qdrant...")
    store_chunks(embedded)

    print("Done.")


if __name__ == "__main__":
    main()
