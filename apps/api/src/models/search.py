from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    user_episode: int = Field(ge=0)
    k: int = Field(default=5, ge=1, le=20)


class SearchResult(BaseModel):
    content: str
    source_url: str
    source_title: str
    entity: str | None
    reveal_episode: int
    distance: float


class SearchResponse(BaseModel):
    results: list[SearchResult]
