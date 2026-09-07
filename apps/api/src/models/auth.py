from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=8)
    access_code: str


class RegisterResponse(BaseModel):
    id: str
    email: str
