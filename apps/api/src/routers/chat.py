from fastapi import APIRouter

from models.chat import ChatRequest, ChatResponse, ChatSource
from services.embeddings import embed_query
from services.llm import complete
from services.prompts import build_messages
from services.reranking import rerank
from services.retrieval import search_chunks

router = APIRouter()

# Candidates pulled by vector search before reranking narrows them down to
# the FINAL_K that actually reach the LLM — see services/reranking.py for why
# a single-stage ranking misses the right chunk.
RETRIEVE_K = 25
FINAL_K = 10


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    query_embedding = await embed_query(request.question)
    candidates = await search_chunks(query_embedding, request.user_episode, RETRIEVE_K)
    chunks = await rerank(request.question, candidates, FINAL_K)
    messages = build_messages(request.question, chunks)
    answer = await complete(messages)
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
    return ChatResponse(answer=answer, sources=sources)