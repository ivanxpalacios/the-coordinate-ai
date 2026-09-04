from fastapi import APIRouter

from models.search import SearchRequest, SearchResponse
from services.embeddings import embed_query
from services.reranking import rerank
from services.retrieval import search_chunks

router = APIRouter()

# Candidates pulled by vector search before reranking narrows them down to
# the caller's requested k — see services/reranking.py for why a
# single-stage ranking misses the right chunk. Widened further when the
# caller asks for more than this many results outright.
RETRIEVE_K = 25


@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    query_embedding = await embed_query(request.query)
    candidates = await search_chunks(
        query_embedding, request.user_episode, max(request.k, RETRIEVE_K)
    )
    results = await rerank(request.query, candidates, request.k)
    return SearchResponse(results=results)
