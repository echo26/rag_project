from scrape.scrape import load_articles
from transform.transform import transform_articles
from metadata.metadata import add_metadata
from store.store import upsert_docs


def main():

    print("[1/4] Scraping articles...")
    articles = load_articles()

    print("[2/4] Transforming to documentation...")
    docs = transform_articles(articles)

    print("[3/4] Adding metadata...")
    docs = add_metadata(docs)

    print("[4/4] Upserting to MongoDB...")
    upsert_docs(docs)

    print("Done.")


if __name__ == "__main__":
    main()
