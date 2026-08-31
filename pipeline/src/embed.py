"""Generates the embedding vector for each chunk (Phase 6, PROJECT.md section 10).

The model is loaded once in main() and passed down, not re-loaded per file:
loading pulls the weights into memory, and doing that 92 times (once per
input file) would be wasted work for no benefit.
"""

import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

CHUNKS_DIR = Path(__file__).resolve().parents[2] / "data" / "chunks"
EMBEDDINGS_DIR = Path(__file__).resolve().parents[2] / "data" / "embeddings"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_chunks(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def embed_directory(subdir: str, model: SentenceTransformer) -> None:
    input_dir = CHUNKS_DIR / subdir
    output_dir = EMBEDDINGS_DIR / subdir
    output_dir.mkdir(parents=True, exist_ok=True)

    for input_path in sorted(input_dir.glob("*.jsonl")):
        output_path = output_dir / input_path.name

        if output_path.exists():
            print(f"[skip] {output_path.name} ya existe")
            continue

        print(f"[embed] {input_path.name}")
        chunks = load_chunks(input_path)
        contents = [chunk["content"] for chunk in chunks]
        embeddings = model.encode(contents)

        lines = [
            json.dumps({**chunk, "embedding": embedding.tolist()}, ensure_ascii=False)
            for chunk, embedding in zip(chunks, embeddings)
        ]
        output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    model = SentenceTransformer(MODEL_NAME)
    embed_directory("episodes", model)
    embed_directory("characters", model)


if __name__ == "__main__":
    main()