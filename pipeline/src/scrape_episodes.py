"""Download season 1 episode wikitext from Fandom's MediaWiki API."""

import json
from pathlib import Path

from mediawiki_client import fetch_wikitext, title_to_page_name

EPISODES_PATH = Path(__file__).resolve().parents[2] / "data" / "episodes.json"
RAW_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "episodes"


def load_season_episodes(season: int) -> list[dict]:
    episodes = json.loads(EPISODES_PATH.read_text(encoding="utf-8"))
    return [ep for ep in episodes if ep["season"] == season]


def output_path(global_number: int, title: str) -> Path:
    slug = title_to_page_name(title)
    return RAW_OUTPUT_DIR / f"{global_number:02d}_{slug}.wikitext"


def scrape_season(season: int) -> None:
    RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    episodes = load_season_episodes(season)

    for episode in episodes:
        path = output_path(episode["global_number"], episode["title"])

        if path.exists():
            print(f"[skip] {path.name} ya existe")
            continue

        print(f"[fetch] {episode['title']}")
        wikitext = fetch_wikitext(episode["title"])
        path.write_text(wikitext, encoding="utf-8")


if __name__ == "__main__":
    scrape_season(season=1)