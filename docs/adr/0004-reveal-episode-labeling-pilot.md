# reveal_episode labeling: episodes vs. characters (pilot)

## 1. Status: Proposed

## 2. Context

Phase 5 of PROJECT.md assigns `reveal_episode` per chunk using a three-step strategy: a heuristic based on manga chapter citations found in the wikitext, LLM assistance for chunks without a citation, and manual review by sampling. This assumed such citations exist in the source wikitext — an assumption also stated in ADR 0002's Consequences section ("manga chapter citations usually appear in the wikitext as `<ref>` tags").

Inspecting the raw wikitext contradicts that assumption: this wiki uses zero `<ref>` tags across every scraped episode and character page, and character "Story" sections contain no inline chapter citations either. The only manga-chapter data available anywhere is the episode-level `Manga chapters` Infobox field, which is already captured in `data/episodes.json` and requires no extraction from the cleaned text. Character chunks (92 total across the pilot set: Eren Yeager, Zeke Yeager, Ymir Fritz) have no textual signal to anchor a chapter-based heuristic to.

## 3. Decision

Episode chunks are labeled by construction: `reveal_episode = episode_number`, the episode the chunk's own article belongs to, since an episode's content cannot leak information from a later episode — no heuristic or LLM pass is needed. Character chunks in the pilot set are labeled fully manually, chunk by chunk, in the order they appear in each character's existing JSONL file (which follows the narrative/arc order of the wiki's "Story" section), cross-referencing `data/episodes.json` for arc and episode boundaries. The resulting `reveal_episode` value is added as a new field to the same JSONL file, rather than a separate output.

## 4. Alternatives considered

(1) Forcing the chapter-based heuristic anyway by inferring implicit chapter boundaries from arc names mentioned in section headings — rejected as too unreliable given zero chapter-level granularity within an arc, and it conflicts with the project's stated safety bias, which favors a correct-but-late `reveal_episode` over a guessed one. (2) Going straight to LLM-assisted labeling for character chunks, skipping manual labeling — rejected for this pilot because there would be no ground truth to validate the LLM's output against, and Phase 1's exit criterion explicitly calls for a manually validated sample.

## 5. Consequences

Episode labeling costs effectively nothing. The 92 manually labeled character chunks double as the validation set required by Phase 1's exit criterion (manual validation of at least 50 chunks at ≥90% accuracy), and the understanding gained from labeling them by hand should inform the design of the future LLM-assisted labeler. This decision does not scale past the pilot's three characters: when the roadmap's Phase 5 (scraping the full four seasons) arrives, an automated or LLM-assisted labeling mechanism still needs to be designed and built — this ADR covers only the pilot, not the long-term mechanism. It also invalidates the citation-based claim in ADR 0002's Consequences section, which should be read as amended by this ADR for this wiki source.

## 6. Date

August 26th, 2026.

## 7. Author

Iván Palacios Martínez
