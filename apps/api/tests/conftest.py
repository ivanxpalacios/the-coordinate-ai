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
    await _create_schema()
    await pool.open(wait=True)
    await _seed_fixture_chunks()
    yield
    await pool.close()