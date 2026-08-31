"""Embeds the user's question so it can be compared against knowledge_chunks.

Must use the same model as pipeline/src/embed.py: the stored vectors and the
query vector only mean something relative to each other if they were produced
by the same model. Loaded once at import time (not per request or lazily) so
the first user question doesn't pay the model-loading cost — see the block-2
plan discussion for the startup-time-vs-first-request-latency trade-off.
"""

import asyncio

from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


async def embed_query(text: str) -> list[float]:
    # model.encode() is a blocking, CPU-bound call. Running it directly in an
    # async def would freeze the event loop for every other in-flight
    # request while it computes, so it's pushed to a worker thread instead.
    embedding = await asyncio.to_thread(model.encode, text)
    return embedding.tolist()
