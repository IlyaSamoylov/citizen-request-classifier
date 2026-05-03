from pydantic import BaseModel

class ClarificationMessage(BaseModel):
    step: int
    question: str
    answer: str | None