import uuid
from pathlib import Path

import psycopg
import pytest_asyncio
from fixtures.chunks import FIXTURE_CHUNKS

from config import settings
from db.pool import pool
from services.embeddings import embed_query

SCHEMA_SQL = Path(__file__).resolve().parents[3] / "pipeline" / "schema.sql"

INSERT_CHUNK = """
    INSERT INTO knowledge_chunks
        (id, content, embedding, source_url, source_title, entity, reveal_episode)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
"""


def _ensure_test_database() -> None:
    # settings.database_url is whatever .env currently points to — if the
    # .env.test -> .env copy step is ever skipped (locally or in CI), this
    # fixture would otherwise create tables and seed FIXTURE_CHUNKS straight
    # into the real Neon database instead of failing loudly.
    if "neon.tech" in settings.database_url:
        raise RuntimeError(
            "settings.database_url points at Neon. Refusing to create the "
            "schema or seed fixture chunks against it — copy .env.test to "
            ".env before running pytest."
        )


async def _create_schema() -> None:
    # A plain, unconfigured connection: the pool's configure step registers
    # the pgvector type, which requires the extension to already exist.
    # Creating it through the pool would deadlock the pool on its own
    # missing dependency, so schema creation must happen before pool.open().
    async with await psycopg.AsyncConnection.connect(settings.database_url) as conn:
        await conn.execute(SCHEMA_SQL.read_text())


async def _seed_fixture_chunks() -> None:
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            for chunk in FIXTURE_CHUNKS:
                chunk_id = uuid.uuid5(uuid.NAMESPACE_URL, f"{chunk['source_url']}#0")
                embedding = await embed_query(chunk["content"])
                await cur.execute(
                    INSERT_CHUNK,
                    (
                        chunk_id,
                        chunk["content"],
                        embedding,
                        chunk["source_url"],
                        chunk["source_title"],
                        chunk["entity"],
                        chunk["reveal_episode"],
                    ),
                )


@pytest_asyncio.fixture(scope="session", autouse=True)
async def open_pool():
    _ensure_test_database()
    await _create_schema()
    await pool.open(wait=True)
    await _seed_fixture_chunks()
    yield
    await pool.close()