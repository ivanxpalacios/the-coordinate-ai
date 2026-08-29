# Character data source: anime pages instead of manga pages

## 1. Status: Proposed

## 2. Context

ADR-0004 selected Eren Yeager, Zeke Yeager, and Ymir Fritz as the pilot's character entities and scraped them from `attackontitan.fandom.com`, treating that wiki as a single, homogeneous source. Inspecting the resulting chunks for Eren revealed that the "Story" section already described events from the Marley arc, the infiltration of Liberio, and the reveal of the Ackerman lineage — content whose place in the narrative is far beyond what a pilot scoped to Season 1 would suggest.

The underlying issue is that `attackontitan.fandom.com` is primarily a manga wiki: a character's default page (e.g. `Eren_Yeager`) narrates their story as told in the manga, not as adapted in the anime. PROJECT.md's scope (section 4.1/4.2) explicitly excludes "manga content beyond what the anime adapts." While the anime does eventually adapt nearly the entire manga, it also cuts, compresses, or reorders some scenes and internal details. A chunk describing content the anime never shows has no valid `reveal_episode` at all — it is a spoiler leak by *source*, not by *episode number*, and no amount of "assign the latest possible episode" (ADR-0004's safety rule) fixes that, since the issue is that the anime never reveals it in the first place.

The same wiki also hosts a separate, dedicated article per character for the anime continuity, suffixed `(Anime)` (e.g. `Eren_Jaeger_(Anime)`, `Zeke_Jaeger_(Anime)`, `Ymir_Fritz_(Anime)`) — same domain, same MediaWiki API, same "Story"/"History"+"Legacy" section structure already relied upon by `scrape_characters.py`.

## 3. Decision

Scrape the `(Anime)` variant of the page for each of the three pilot characters instead of the manga-default page, keeping the same three entities (Eren, Zeke, Ymir) and the same section names per entity, since the access mechanism (ADR-0002) and section structure are unchanged. `scrape_characters.py`'s `ENTITIES` dict now keys on the anime page titles ("Eren Jaeger (Anime)", "Zeke Jaeger (Anime)", "Ymir Fritz (Anime)"). Because the anime page title uses a different spelling of the surname ("Jaeger" instead of "Yeager") and carries the `(Anime)` suffix, `chunk.py`'s `parse_source` strips the suffix when deriving the `entity` metadata field, adopting "Jaeger" as the canonical spelling going forward; `source_title`/`source_url` are left untouched since they should reflect the actual source page.

## 4. Alternatives considered

(1) Keep scraping the manga-default pages and rely on manual judgment during labeling to discard chunks describing content never shown in the anime — rejected because it pushes a preventable problem onto human review instead of fixing it at the source, and manual review is exactly the step most likely to miss an anime/manga divergence buried in 90+ chunks. (2) Replace Zeke and Ymir with Mikasa and Armin instead of switching source — considered and rejected: it was motivated by preference, not by the actual problem, and it would have changed the pilot's risk profile away from ADR-0004's explicit rationale (prioritizing the entities most central to the Founding Titan/Titan Shifter secrets) without addressing the manga-vs-anime leak at all.

## 5. Consequences

The 92 character chunks previously scraped and partially labeled from the manga-default pages are invalidated and were deleted (`data/raw/characters`, `data/processed/characters`, `data/chunks/characters`); they are replaced by 98 chunks re-scraped from the anime pages, and the manual `reveal_episode` labeling restarts from zero on this new set. This does not eliminate every risk: the anime pages could themselves contain manga-only asides or errors introduced by wiki editors, so the same source-level vigilance (does the anime actually show this, before asking in which episode) still applies during manual labeling — it is reduced, not removed. It also raises an open question for Phase 5 (scaling to more entities): each new character must be checked individually for the existence of an `(Anime)` page; where one does not exist, the same manual caution used here will need to be applied by hand.

## 6. Date

August 27th, 2026.

## 7. Author

Iván Palacios Martínez
