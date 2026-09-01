from fastapi import APIRouter

from models.search import SearchRequest, SearchResponse
from services.embeddings import embed_query
from services.retrieval import search_chunks

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    query_embedding = await embed_query(request.query)
    results = await search_chunks(query_embedding, request.user_episode, request.k)
    return SearchResponse(results=results)
