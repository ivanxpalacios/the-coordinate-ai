"""Download season 1 episode wikitext from Fandom's MediaWiki API.

Source and justification: docs/adr/0002-source-of-scraping-api-mediawiki.md
"""

import json
import time
from pathlib import Path

import requests

API_URL = "https://attackontitan.fandom.com/api.php"
USER_AGENT = (
    "the-coordinate-ai-bot/0.1 (fanmade non-commercial project; "
    "contact: ivanpalaciosdev@gmail.com)"
)
REQUEST_DELAY_SECONDS = 1.5

EPISODES_PATH = Path(__file__).resolve().parents[2] / "data" / "episodes.json"
RAW_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "episodes"


def load_season_episodes(season: int) -> list[dict]:
    episodes = json.loads(EPISODES_PATH.read_text(encoding="utf-8"))
    return [ep for ep in episodes if ep["season"] == season]


def title_to_page_name(title: str) -> str:
    return title.replace(" ", "_")


def output_path(global_number: int, title: str) -> Path:
    slug = title_to_page_name(title)
    return RAW_OUTPUT_DIR / f"{global_number:02d}_{slug}.wikitext"


def fetch_wikitext(title: str) -> str:
    page_name = title_to_page_name(title)
    params = {
        "action": "parse",
        "page": page_name,
        "format": "json",
        "prop": "wikitext",
    }
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(API_URL, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    payload = response.json()

    if "error" in payload:
        raise RuntimeError(f"MediaWiki API error for '{page_name}': {payload['error']}")

    return payload["parse"]["wikitext"]["*"]


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

        time.sleep(REQUEST_DELAY_SECONDS)


if __name__ == "__main__":
    scrape_season(season=1)
