"""Loads embedded chunks into Postgres/pgvector (Phase 6, PROJECT.md section 10).

Each row is upserted, not inserted blindly: id is deterministic (uuid5 from
source_url + chunk_index), so re-running this script after a labeling fix
updates the existing row instead of erroring on a duplicate key.
"""

import json
import os
import uuid
from pathlib import Path

import numpy as np
import psycopg
from dotenv import load_dotenv
from pgvector.psycopg import register_vector

EMBEDDINGS_DIR = Path(__file__).resolve().parents[2] / "data" / "embeddings"

UPSERT_QUERY = """
    INSERT INTO knowledge_chunks
        (id, content, embedding, source_url, source_title, entity, reveal_episode)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO UPDATE SET
        content = EXCLUDED.content,
        embedding = EXCLUDED.embedding,
        source_url = EXCLUDED.source_url,
        source_title = EXCLUDED.source_title,
        entity = EXCLUDED.entity,
        reveal_episode = EXCLUDED.reveal_episode
"""


def load_chunks(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def make_id(source_url: str, chunk_index: int) -> uuid.UUID:
    return uuid.uuid5(uuid.NAMESPACE_URL, f"{source_url}#{chunk_index}")


def chunk_to_row(chunk: dict) -> tuple:
    return (
        make_id(chunk["source_url"], chunk["chunk_index"]),
        chunk["content"],
        np.array(chunk["embedding"]),
        chunk["source_url"],
        chunk["source_title"],
        chunk["entity"],
        chunk["reveal_episode"],
    )


def ingest_directory(subdir: str, conn: psycopg.Connection) -> None:
    input_dir = EMBEDDINGS_DIR / subdir

    for input_path in sorted(input_dir.glob("*.jsonl")):
        print(f"[ingest] {input_path.name}")
        chunks = load_chunks(input_path)
        rows = [chunk_to_row(chunk) for chunk in chunks]

        with conn.cursor() as cur:
            cur.executemany(UPSERT_QUERY, rows)
        conn.commit()


def main() -> None:
    load_dotenv()
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        register_vector(conn)
        ingest_directory("episodes", conn)
        ingest_directory("characters", conn)


if __name__ == "__main__":
    main()