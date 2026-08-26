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
