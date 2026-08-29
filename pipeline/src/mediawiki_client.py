"""Shared HTTP client for the Fandom MediaWiki API.

Source and rationale: docs/adr/0002-source-of-scraping-api-mediawiki.md
"""

import time

import requests

API_URL = "https://attackontitan.fandom.com/api.php"
USER_AGENT = (
    "the-coordinate-ai-bot/0.1 (fanmade non-commercial project; "
    "contact: ivanpalaciosdev@gmail.com)"
)
REQUEST_DELAY_SECONDS = 1.5


def title_to_page_name(title: str) -> str:
    return title.replace(" ", "_")


def _request_wikitext(title: str) -> str:
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

    time.sleep(REQUEST_DELAY_SECONDS)
    return payload["parse"]["wikitext"]["*"]


def fetch_wikitext(title: str) -> str:
    """Fetches a page's wikitext, retrying once with a "(Episode)" suffix if the
    bare title turns out to belong to something else on this wiki.

    Some titles collide with a manga chapter of the same name: the bare title
    either doesn't exist (missingtitle error) or is itself a redirect to the
    chapter page (wikitext starting with "#REDIRECT"), and the real episode
    article lives at "{title} (Episode)" instead.
    """
    try:
        wikitext = _request_wikitext(title)
    except RuntimeError:
        return _request_wikitext(f"{title} (Episode)")

    if wikitext.startswith("#REDIRECT"):
        return _request_wikitext(f"{title} (Episode)")
    return wikitext
