# Chunking strategy for processed wikitext

## 1. Status: Accepted

## 2. Context

Phase 4 (PROJECT.md) requires splitting cleaned text by semantic unit rather than by a fixed character count, targeting 200-400 tokens per chunk, with `reveal_episode` still to be assigned per chunk in Phase 5. The LLM provider (D-01) and the embeddings model (D-02) remain undecided, so the chunker cannot assume a specific tokenizer.

## 3. Decision

Split in two passes. First, paragraphs (separated by blank lines) that exceed 400 estimated tokens are subdivided by grouping consecutive sentences up to that limit. Second, the resulting units that fall below 200 estimated tokens are merged forward into a buffer until the minimum is reached; any trailing remainder at the end of a document is merged backward into the previous chunk instead of becoming an undersized orphan. Token count is approximated as `word_count * 1.3`, with no real tokenizer involved. Output is JSONL, one file per source article, written to `data/chunks/{episodes,characters}/`, mirroring the per-file, skip-if-exists pattern already used by `clean_directory`. Each chunk record carries `source_url`, `source_title`, `source_type`, `episode_number` (episodes) or `entity` (characters), and `chunk_index` — all reconstructed from the input filename, since the scraper does not persist a separate metadata file (the MediaWiki page title is already encoded in the filename via `title_to_page_name`).

## 4. Alternatives considered

(1) Using a real tokenizer (e.g. `tiktoken`) for the token estimate — rejected for now because committing to a specific tokenizer's counting semantics is premature while D-01/D-02 are open, and 200-400 tokens is a soft target rather than a hard limit; the hard limit will be validated in `embed.py` once a model is chosen. (2) Fixed-size character/token chunking — rejected because it directly contradicts Phase 4's requirement to split by semantic unit rather than a fixed count, and risks cutting a self-contained fact in half. (3) A single consolidated JSON/JSONL file for all chunks — rejected because it would break the incremental, idempotent, re-runnable pattern already established by `clean_directory`, which Phase 6 requires of the whole pipeline.

## 5. Consequences

Chunk sizes stay close to the target range without ad hoc truncation, and the metadata schema already provides the per-chunk anchor (`episode_number` or `entity`) that `label.py` needs. The word-count-based token estimate is an approximation that may drift from the real tokenizer of whichever model is eventually chosen, so chunk sizes may need re-validation once D-01/D-02 are resolved. The sentence splitter is a simple regex over `. ! ?` and mis-splits on abbreviations (e.g. "Mr.", "Dr.") — a known limitation, acceptable for the spike and to be audited during the manual review in Phase 5, step 3.

## 6. Date

August 26th, 2026.

## 7. Author

Iván Palacios Martínez
