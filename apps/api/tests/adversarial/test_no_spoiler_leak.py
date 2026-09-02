"""Layer 1 of the anti-spoiler defense (PROJECT.md section 11): the WHERE
reveal_episode <= user_episode filter must never let a later-revealed chunk
through, no matter what the query asks for.
"""

import pytest

from cases import CASES
from services.embeddings import embed_query
from services.retrieval import search_chunks


@pytest.mark.parametrize("case", CASES, ids=[c.description for c in CASES])
async def test_no_spoiler_leak(case):
    embedding = await embed_query(case.query)
    results = await search_chunks(embedding, case.user_episode, k=20)

    leaks = [r for r in results if r["reveal_episode"] > case.user_episode]
    assert not leaks, f"Spoiler leak in '{case.description}': {leaks}"
