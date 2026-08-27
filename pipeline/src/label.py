"""Assigns reveal_episode to episode chunks (ADR-0004).

Episode chunks are labeled by construction: reveal_episode = episode_number,
a field chunk.py already writes into each JSONL line from the filename
(parse_source). This module does not re-derive it from the filename to
avoid a second, divergent source of truth for the same fact.

Character chunks are out of scope: ADR-0004 labels them manually, chunk by
chunk, directly in their JSONL files.
"""

import json
import os
from pathlib import Path

CHUNKS_DIR = Path(__file__).resolve().parents[2] / "data" / "chunks"


def label_episode_chunk(chunk: dict) -> dict:
    if chunk["source_type"] != "episode":
        raise ValueError(f"expected an episode chunk, got source_type={chunk['source_type']!r}")
    return {**chunk, "reveal_episode": chunk["episode_number"]}


def label_file(path: Path) -> None:
    """Streams line by line: never holds the whole file in memory, and the
    original is only replaced once the temp file is fully written.
    """
    tmp_path = path.with_suffix(path.suffix + ".tmp")

    try:
        with path.open("r", encoding="utf-8") as src, tmp_path.open("w", encoding="utf-8") as dst:
            for line in src:
                chunk = label_episode_chunk(json.loads(line))
                dst.write(json.dumps(chunk, ensure_ascii=False) + "\n")

        os.replace(tmp_path, path)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise


def main() -> None:
    for path in sorted((CHUNKS_DIR / "episodes").glob("*.jsonl")):
        print(f"[label] {path.name}")
        label_file(path)


if __name__ == "__main__":
    main()