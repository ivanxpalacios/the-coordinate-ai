from fastapi import APIRouter

from models.chat import ChatRequest, ChatResponse, ChatSource
from services.embeddings import embed_query
from services.llm import complete
from services.prompts import build_messages
from services.retrieval import search_chunks

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    query_embedding = await embed_query(request.question)
    chunks = await search_chunks(query_embedding, request.user_episode)
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