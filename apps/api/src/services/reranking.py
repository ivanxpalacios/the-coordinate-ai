"""Reorders retrieval candidates by actual question-passage relevance.

Vector similarity (services/retrieval.py) ranks by embedding distance, which
favors chunks that are lexically/topically dense in the query's terms — not
necessarily the chunk that answers the question. A cross-encoder scores each
(query, passage) pair directly, so it catches passages like "Armin reveals
Annie is the Female Titan" even when they mention the query terms only once.

Must run on a wider candidate set than the final k (see retrieval callers):
reranking only helps if the right chunk was retrieved at all.
"""

import asyncio

from sentence_transformers import CrossEncoder

MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

model = CrossEncoder(MODEL_NAME)


async def rerank(query: str, chunks: list[dict], top_k: int) -> list[dict]:
    if not chunks:
        return []

    pairs = [(query, chunk["content"]) for chunk in chunks]
    # model.predict() is a blocking, CPU-bound call — same reasoning as
    # embed_query in services/embeddings.py.
    scores = await asyncio.to_thread(model.predict, pairs)

    ranked = sorted(zip(scores, chunks), key=lambda pair: pair[0], reverse=True)
    return [chunk for _, chunk in ranked[:top_k]]
