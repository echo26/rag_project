from source.source import load_articles
from transform.transform import transform_articles
from store.store import upsert_docs


def main():

    print("[1/3] Scraping articles...")
    articles = load_articles()

    print("[2/3] Transforming to documentation...")
    docs = transform_articles(articles)

    print("[3/3] Upserting to MongoDB...")
    upsert_docs(docs)

    print("Done.")


if __name__ == "__main__":
    main()
