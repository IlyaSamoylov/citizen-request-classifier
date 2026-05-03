from pydantic import BaseModel, Field
from datetime import datetime

class ClarificationMessage(BaseModel):
    step: int
    question: str
    answer: str | None = None
    created_at: datetime


class ClarificationAnswerIn(BaseModel):
    answer: str = Field(min_length=1, max_length=1000)