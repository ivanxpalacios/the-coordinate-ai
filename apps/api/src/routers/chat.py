import json
from collections.abc import AsyncIterator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from models.chat import ChatRequest, ChatSource
from services.embeddings import embed_query
from services.llm import LlmError, stream_complete
from services.prompts import build_messages
from services.reranking import rerank
from services.retrieval import search_chunks

router = APIRouter()

# Candidates pulled by vector search before reranking narrows them down to
# the FINAL_K that actually reach the LLM — see services/reranking.py for why
# a single-stage ranking misses the right chunk.
RETRIEVE_K = 25
FINAL_K = 10


def _sse(payload: dict) -> str:
    return f"data: {json.dumps(payload)}\n\n"


async def _stream_chat(request: ChatRequest) -> AsyncIterator[str]:
    query_embedding = await embed_query(request.question)
    candidates = await search_chunks(query_embedding, request.user_episode, RETRIEVE_K)
    chunks = await rerank(request.question, candidates, FINAL_K)
    sources = [
        ChatSource(
            chunk_id=c["id"],
            source_title=c["source_title"],
            source_url=c["source_url"],
            entity=c["entity"],
            global_number=c["reveal_episode"],
        )
        for c in chunks
    ]
    yield _sse({"type": "sources", "sources": [s.model_dump(mode="json") for s in sources]})

    messages = build_messages(request.question, chunks)
    try:
        async for delta in stream_complete(messages):
            yield _sse({"type": "token", "content": delta})
    except LlmError as e:
        yield _sse({"type": "error", "message": str(e)})
        return
    yield _sse({"type": "done"})


@router.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    return StreamingResponse(_stream_chat(request), media_type="text/event-stream")