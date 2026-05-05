from pydantic import BaseModel, Field
from datetime import datetime

class ClarificationMessage(BaseModel):
    step: int = Field(ge=1)
    question: str = Field(min_length=1)
    answer: str | None = Field(default=None, max_length=1000)
    created_at: datetime


class ClarificationAnswerIn(BaseModel):
    answer: str = Field(min_length=1, max_length=1000)