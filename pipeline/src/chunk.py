"""Splits processed plain text into semantic chunks, including source metadata.

A two-pass strategy to approach the target range of 200–400 tokens
(PROJECT.md, Phase 4) without splitting based on a fixed character count:

1. Paragraphs exceeding MAX_CHUNK_TOKENS are subdivided by grouping
consecutive sentences (split_oversized_paragraph).
2. Resulting units falling below MIN_CHUNK_TOKENS are merged with
subsequent units until the minimum is reached (merge_undersized_units).

Known limitations, acceptable for the spike (to be audited during the
manual review in Phase 5, step 3):
- Sentence splitting relies on a simple regex using '. ! ?'; it fails with
abbreviations (e.g., "Mr.", "Dr.").
- If a single sentence exceeds MAX_CHUNK_TOKENS, it is not subdivided further.
- There is no metadata file separate from the scraper; source_url and
source_title are reconstructed from the filename, which already
encodes the MediaWiki page title (see title_to_page_name in
mediawiki_client.py).
"""

import json
import re
from pathlib import Path

PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"
CHUNKS_DIR = Path(__file__).resolve().parents[2] / "data" / "chunks"

BASE_URL = "https://attackontitan.fandom.com/wiki/"

HEADER_PATTERN = re.compile(r"^=+\s*.+?\s*=+$")
SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")
EPISODE_FILENAME_PATTERN = re.compile(r"^(\d{2})_(.+)$")

MIN_CHUNK_TOKENS = 200
MAX_CHUNK_TOKENS = 400
TOKENS_PER_WORD = 1.3


def estimate_tokens(text: str) -> int:
    """Approach without an actual tokenizer: avoiding commitment to a model that has not yet been selected (D-01/D-02)."""
    return round(len(text.split()) * TOKENS_PER_WORD)


def split_into_paragraphs(text: str) -> list[str]:
    """Separate by blank lines, discarding stray header lines."""
    paragraphs = []
    for block in text.split("\n\n"):
        lines = [line for line in block.splitlines() if not HEADER_PATTERN.match(line.strip())]
        paragraph = "\n".join(lines).strip()
        if paragraph:
            paragraphs.append(paragraph)
    return paragraphs


def split_into_sentences(paragraph: str) -> list[str]:
    return [s.strip() for s in SENTENCE_SPLIT_PATTERN.split(paragraph) if s.strip()]


def split_oversized_paragraph(paragraph: str) -> list[str]:
    if estimate_tokens(paragraph) <= MAX_CHUNK_TOKENS:
        return [paragraph]

    groups = []
    current: list[str] = []
    current_tokens = 0

    for sentence in split_into_sentences(paragraph):
        sentence_tokens = estimate_tokens(sentence)
        if current and current_tokens + sentence_tokens > MAX_CHUNK_TOKENS:
            groups.append(" ".join(current))
            current = []
            current_tokens = 0
        current.append(sentence)
        current_tokens += sentence_tokens

    if current:
        groups.append(" ".join(current))

    return groups


def merge_undersized_units(units: list[str]) -> list[str]:
    chunks = []
    buffer: list[str] = []
    buffer_tokens = 0

    for unit in units:
        buffer.append(unit)
        buffer_tokens += estimate_tokens(unit)
        if buffer_tokens >= MIN_CHUNK_TOKENS:
            chunks.append("\n\n".join(buffer))
            buffer = []
            buffer_tokens = 0

    if buffer:
        leftover = "\n\n".join(buffer)
        if chunks:
            chunks[-1] = f"{chunks[-1]}\n\n{leftover}"
        else:
            chunks.append(leftover)

    return chunks


def chunk_text(text: str) -> list[str]:
    paragraphs = split_into_paragraphs(text)
    units = [unit for paragraph in paragraphs for unit in split_oversized_paragraph(paragraph)]
    return merge_undersized_units(units)


def parse_source(subdir: str, stem: str) -> dict:
    """Reconstructs source_url/source_title/entity from the filename."""
    if subdir == "episodes":
        match = EPISODE_FILENAME_PATTERN.match(stem)
        slug = match.group(2)
        return {
            "source_url": BASE_URL + slug,
            "source_title": slug.replace("_", " "),
            "source_type": "episode",
            "episode_number": int(match.group(1)),
            "entity": None,
        }

    return {
        "source_url": BASE_URL + stem,
        "source_title": stem.replace("_", " "),
        "source_type": "character",
        "episode_number": None,
        "entity": stem.replace("_", " "),
    }


def chunk_directory(subdir: str) -> None:
    input_dir = PROCESSED_DIR / subdir
    output_dir = CHUNKS_DIR / subdir
    output_dir.mkdir(parents=True, exist_ok=True)

    for input_path in sorted(input_dir.glob("*.txt")):
        output_path = output_dir / f"{input_path.stem}.jsonl"

        if output_path.exists():
            print(f"[skip] {output_path.name} ya existe")
            continue

        print(f"[chunk] {input_path.name}")
        source = parse_source(subdir, input_path.stem)
        chunks = chunk_text(input_path.read_text(encoding="utf-8"))

        lines = [
            json.dumps({"content": content, "chunk_index": index, **source}, ensure_ascii=False)
            for index, content in enumerate(chunks)
        ]
        output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    chunk_directory("episodes")
    chunk_directory("characters")


if __name__ == "__main__":
    main()