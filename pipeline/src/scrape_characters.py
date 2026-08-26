"""Download the "Story" section of entity pages from the Fandom MediaWiki API.

See docs/adr/0002-source-of-scraping-api-mediawiki.md for the access mechanism,
and the discussion in Eren's block for the rationale behind limiting the scope
to the "Story" section.
"""

import re
from pathlib import Path

from mediawiki_client import fetch_wikitext, title_to_page_name

RAW_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "characters"

# Entity title -> wikitext sections to extract and concatenate.
# Most characters have a "Story" section narrated arc by arc.
# Ymir Fritz does not appear in real-time within the plot, so her page
# lacks a "Story" section; instead, it uses "History" (biography) + "Legacy" (subsequent impact).
ENTITIES: dict[str, list[str]] = {
    "Eren Yeager": ["Story"],
    "Zeke Yeager": ["Story"],
    "Ymir Fritz": ["History", "Legacy"],
}


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

    for title, section_names in ENTITIES.items():
        path = output_path(title)

        if path.exists():
            print(f"[skip] {path.name} ya existe")
            continue

        print(f"[fetch] {title}")
        wikitext = fetch_wikitext(title)
        sections = [extract_section(wikitext, name) for name in section_names]
        path.write_text("\n\n".join(sections), encoding="utf-8")


if __name__ == "__main__":
    scrape_entities()