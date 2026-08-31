"""Vector search over knowledge_chunks, filtered by spoiler layer 1
(PROJECT.md section 11): reveal_episode <= user_episode is applied in the
WHERE clause, before ranking by similarity, so filtered-out chunks never
reach the ORDER BY step.
"""

from psycopg.rows import dict_row

from db.pool import pool

SEARCH_QUERY = """
    SELECT content, source_url, source_title, entity, reveal_episode,
           embedding <=> %s::vector AS distance
    FROM knowledge_chunks
    WHERE reveal_episode <= %s
    ORDER BY distance
    LIMIT %s
"""


async def search_chunks(
    query_embedding: list[float], user_episode: int, k: int = 5
) -> list[dict]:
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(SEARCH_QUERY, (query_embedding, user_episode, k))
            return await cur.fetchall()
