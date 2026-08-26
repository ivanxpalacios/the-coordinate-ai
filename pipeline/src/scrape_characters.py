"""Download the "Story" section of entity pages from the Fandom MediaWiki API.

See docs/adr/0002-source-of-scraping-api-mediawiki.md for the access mechanism,
and the discussion in Eren's block for the rationale behind limiting the scope
to the "Story" section.
"""

import re
from pathlib import Path

from mediawiki_client import fetch_wikitext, title_to_page_name

RAW_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "characters"
SECTION_TO_EXTRACT = "Story"
ENTITIES = ["Eren Yeager"]


def extract_section(wikitext: str, section_title: str) -> str:
    start_pattern = re.compile(rf"(?m)^==\s*{re.escape(section_title)}\s*==\s*$")
    match = start_pattern.search(wikitext)

    if not match:
        raise ValueError(f"Section '{section_title}' not found in wikitext")

    next_heading = re.search(r"(?m)^==[^=].*==\s*$", wikitext[match.end() :])
    end = match.end() + next_heading.start() if next_heading else len(wikitext)

    return wikitext[match.start() : end].strip()


def output_path(title: str) -> Path:
    slug = title_to_page_name(title)
    return RAW_OUTPUT_DIR / f"{slug}.wikitext"


def scrape_entities() -> None:
    RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for title in ENTITIES:
        path = output_path(title)

        if path.exists():
            print(f"[skip] {path.name} ya existe")
            continue

        print(f"[fetch] {title}")
        wikitext = fetch_wikitext(title)
        section = extract_section(wikitext, SECTION_TO_EXTRACT)
        path.write_text(section, encoding="utf-8")


if __name__ == "__main__":
    scrape_entities()