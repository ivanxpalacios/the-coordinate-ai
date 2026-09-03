import uuid

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    user_episode: int = Field(ge=0)


class ChatSource(BaseModel):
    chunk_id: uuid.UUID
    source_title: str
    source_url: str
    entity: str | None
    global_number: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSource]
