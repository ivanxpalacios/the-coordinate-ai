# Source of scraping API Mediawiki

## 1. Status: Proposed

## 2. Context

What was tried first (direct HTML requests to Fandom pages), what was found (Cloudflare blocks access with a JS challenge; even `robots.txt` returns the challenge instead of actual rules), and why this matters (there is no reliable way to determine if HTML scraping is permitted, nor to execute it without solving a JS challenge)

## 3. Decision

Use the `action=parse` endpoint of the public MediaWiki API (`/api.php`) exposed by Fandom, requesting wikitext instead of rendered HTML.

## 4. Alternatives considered

(a) solving the Cloudflare challenge using a headless browser—rejected due to complexity and because it crosses the line from "legitimate access" to actively bypassing a protection mechanism; (b) using a Fandom data dump (if one exists)—to be evaluated if you wish to explore this as a future alternative

## 5. Consequences

Positive: wikitext comes with delimited sections (e.g., `==Synopsis==`), simplifying Phase 3 (cleaning) and Phase 5 (labeling, as manga chapter citations usually appear in the wikitext as `<ref>` tags).

This endpoint is not officially documented by Fandom as being for "free use"—it represents a non-contractual dependency. If it changes or is restricted, the entire ingestion pipeline will break.

Relation to D-06: this resolves half of that open decision (the access mechanism); the exact scope of pages/entities—which was already being defined separately—remains to be finalized.

## 6. Date

August 26th, 2026.

## 7. Author

Iván Palacios Martínez

## 8. Amendment (2026-08-29): title collisions with manga chapter pages

While scraping episodes 26-89, 54 of the 89 episode titles turned out to collide with a manga chapter of the same name on this wiki. In that case the bare title belongs to the chapter, not the episode: the API either returns a `missingtitle` error or, more insidiously, silently returns a one-line `#REDIRECT [[Title (Chapter)]]` stub as if it were valid wikitext — this second case does not raise an error and was initially missed, producing 54 chunk files whose entire content was that redirect stub instead of the actual episode narration.

The real episode article lives at `"{title} (Episode)"` in every one of these 54 cases. `mediawiki_client.fetch_wikitext` now retries once with that suffix whenever the initial request either raises a `missingtitle` error or returns wikitext starting with `#REDIRECT`, before giving up.

One further exception did not fit even that pattern: episode 57 ("That Day") collides with another episode (episode 2), not a chapter, and the wiki disambiguates it as `"That Day (Episode 57)"` rather than the generic `"(Episode)"` suffix. Since this is a title shared between two episodes — not expected to recur — it is handled with a manual `wiki_title` override field in `episodes.json`, read by `scrape_episodes.py` in place of `title` when present, rather than generalizing the client's fallback to a second, number-based suffix for a single occurrence.
