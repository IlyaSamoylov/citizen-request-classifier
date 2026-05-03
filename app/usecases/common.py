from dataclasses import dataclass
from datetime import datetime

from app.schemas.clarification import ClarificationMessage

@dataclass
class CreateRequestResult:
    request_id: int
    raw_text: str
    is_toxic: bool
    categories: list[dict]
    created_at: datetime
    clarification_needed: bool = False
    clarification_question: str | None = None

@dataclass
class GetRequestResult:
    request_id: int
    raw_text: str
    is_toxic: bool
    categories: list[dict]
    clarifications: list[ClarificationMessage]
    created_at: datetime
    updated_at: datetime | None

def to_request_result(request) -> GetRequestResult:
    categories = [
        {
            "code": rc.category.code,
            "confidence": rc.confidence,
        }
        for rc in request.request_categories
    ]

    clarifications = [
        ClarificationMessage(
            question=c.question,
            answer=c.answer,
            step=c.step,
            created_at=c.created_at,
        )
        for c in request.clarifications
    ]

    return GetRequestResult(
        request_id=request.id,
        raw_text=request.raw_text,
        is_toxic=request.is_toxic,
        categories=categories,
        clarifications=clarifications,
        created_at=request.created_at,
        updated_at=request.updated_at,
    )