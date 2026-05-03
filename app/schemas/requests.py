from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.clarification import ClarificationMessage

class RequestIn(BaseModel):
    text: str = Field(min_length=1, max_length=500)

class RequestCategoryOut(BaseModel):
    code: str
    confidence: float | None = None

class RequestOut(BaseModel):
    id: int
    raw_text: str
    categories: list[RequestCategoryOut]
    is_toxic: bool
    clarification_question: str | None = None
    created_at: datetime


class RequestFull(BaseModel):
    id: int
    raw_text: str
    categories: list[RequestCategoryOut]
    is_toxic: bool
    clarifications: list[ClarificationMessage]
    created_at: datetime
    updated_at: datetime | None
