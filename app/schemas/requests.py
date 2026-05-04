from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.clarification import ClarificationMessage

class RequestIn(BaseModel):
    text: str = Field(min_length=1, max_length=500)

class RequestCategoryOut(BaseModel):
    code: str = Field(min_length=1)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)

class RequestOut(BaseModel):
    id: int = Field(gt=0)
    raw_text: str = Field(min_length=1, max_length=500)
    categories: list[RequestCategoryOut]
    is_toxic: bool
    clarification_question: str | None = None
    created_at: datetime


class RequestFull(BaseModel):
    id: int = Field(gt=0)
    raw_text: str = Field(min_length=1, max_length=500)
    categories: list[RequestCategoryOut] = Field(min_length=0) #TODO: ТОЛЬКО ПОКА НЕТ БАЗЫ, ПОТОМ min_length=1
    is_toxic: bool
    clarifications: list[ClarificationMessage]
    created_at: datetime
    updated_at: datetime | None
