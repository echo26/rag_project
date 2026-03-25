import json
import logging
import mwxml
import mwparserfromhell

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DUMP_FILE = "simplewiki-latest-pages-articles.xml"
OUTPUT_FILE = "simplewiki.jsonl"
MIN_TEXT_LENGTH = 100


def xml2json():
    dump = mwxml.Dump.from_file(open(DUMP_FILE, encoding="utf-8"))
    count = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for page in dump.pages:
            if page.namespace != 0:
                continue

            for revision in page:
                wikicode = mwparserfromhell.parse(revision.text or "")
                plain_text = wikicode.strip_code(
                    normalize=True, collapse=True, keep_template_params=False
                )

                if (
                    plain_text.startswith("#REDIRECT")
                    or len(plain_text) < MIN_TEXT_LENGTH
                ):
                    break

                out.write(
                    json.dumps(
                        {
                            "id": page.id,
                            "title": page.title,
                            "text": plain_text.strip(),
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
                count += 1
                if count % 1000 == 0:
                    logger.info(f"Processed {count} articles...")
                break  # only latest revision

    logger.info(f"Done. {count} articles written to {OUTPUT_FILE}")


if __name__ == "__main__":
    xml2json()
