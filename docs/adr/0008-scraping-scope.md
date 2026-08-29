# Scraping and chunking scope for MVP (D-06)

## 1. Status: Proposed

## 2. Context

PROJECT.md's roadmap leaves D-06 (exact scraping source and scope) open, distinct from ADR-0005, which fixed which page variant to scrape for the three pilot characters but did not decide how many entities or how much of the show's runtime the MVP should cover.

## 3. Decision

Episodes: scrape and chunk all four seasons (89 episodes), not just Season 1. Characters: keep the MVP limited to the three pilot entities already labeled (Eren Jaeger, Zeke Jaeger, Ymir Fritz) — no additional character pages are scraped before launch.

## 4. Alternatives considered

Scraping additional character pages before launch (e.g. Mikasa, Armin, Reiner) — rejected for the MVP: ADR-0004 already flagged that manual `reveal_episode` labeling does not scale past the pilot's three characters, and each new character reproduces that same manual-labeling cost with no automated alternative built yet. Limiting episodes to Season 1 only, mirroring the original spike scope — rejected: full-season episode chunks are labeled by construction (`reveal_episode = episode_number`, per ADR-0004) at effectively no extra manual cost, and they already carry meaningful character information through episode narration, partially offsetting the narrower character coverage.

## 5. Consequences

The MVP's character-specific retrieval will be shallower for any character outside Eren, Zeke, and Ymir Fritz — questions about e.g. Reiner or Historia will only be answerable from episode-level chunks that mention them, not from a dedicated character biography. This is accepted as a deliberate MVP scope cut, not an oversight. Expanding character coverage after launch is expected to be incremental at the pipeline level (new entities are new files/rows, per ADR-0003's skip-if-exists pattern and Phase 6's idempotent ingestion), but is blocked on designing an LLM-assisted `reveal_episode` labeler — proposed for that future work: comparing a new character chunk against already-labeled episode chunks describing the same event, to infer the matching `reveal_episode` instead of manual labeling from scratch. That labeler is explicitly out of scope for this ADR and for the MVP.

## 6. Date

August 29th, 2026.

## 7. Author

Iván Palacios Martínez
