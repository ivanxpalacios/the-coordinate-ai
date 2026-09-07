"""Regression test for the retrieval recall bug (see project memory / chat
history): vector similarity alone ranked the episode-17 chunk (dense in the
literal phrase "Female Titan") above the episode-23 chunk that actually
reveals Annie's identity. Reranking must fix that ordering.
"""

from services.reranking import rerank

DENSE_BUT_WRONG = {
    "id": 1,
    "reveal_episode": 17,
    "content": (
        "Female Titan: The 57th Exterior Scouting Mission, Part 1 is the "
        "17th episode of the 1st season and the 17th episode overall of the "
        "Attack on Titan anime, produced by Wit Studio and Production I.G. "
        "Erwin's long distance enemy scouting formation proceeds towards "
        "Shiganshina as expected until Armin encounters a Female Titan. "
        "Joining Reiner and Jean, the three confront the Titan to buy the "
        "commander time."
    ),
}

ANSWERS_THE_QUESTION = {
    "id": 2,
    "reveal_episode": 23,
    "content": (
        "Armin finally reveals his suspicion that Annie is the Female Titan "
        "since the omni-directional mobility gear she had presented to "
        "check for unauthorized usage after Sawney and Beane were killed "
        "was Marco's."
    ),
}


async def test_rerank_prefers_chunk_that_answers_the_question():
    candidates = [DENSE_BUT_WRONG, ANSWERS_THE_QUESTION]

    results = await rerank("Who is the Female Titan?", candidates, top_k=1)

    assert results[0]["id"] == ANSWERS_THE_QUESTION["id"]


async def test_rerank_returns_empty_for_no_candidates():
    assert await rerank("Who is the Female Titan?", [], top_k=5) == []
