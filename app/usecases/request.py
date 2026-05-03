from dataclasses import dataclass
from datetime import datetime
from app.db.uow import UnitOfWork
from app.repos.category_repo import CategoryRepository
from app.repos.clarification_repo import ClarificationRepository
from app.repos.request_repo import RequestRepository


@dataclass
class CreateRequestResult:
    request_id: int
    raw_text: str
    is_toxic: bool
    categories: list[dict]
    created_at: datetime
    clarification_needed: bool = False
    clarification_question: str | None = None


class RequestUseCase:
    def __init__(self, classifier, toxicity_detector):
        self.classifier = classifier
        self.toxicity_detector = toxicity_detector

    async def create(self, uow: UnitOfWork, text: str) -> CreateRequestResult:
        request_repo = RequestRepository(uow.session)
        category_repo = CategoryRepository(uow.session)
        clarification_repo = ClarificationRepository(uow.session)

        is_toxic = await self.toxicity_detector.detect(text)

        request = await request_repo.create(raw_text=text, is_toxic=is_toxic)

        prediction = await self.classifier.predict(text)

        valid_codes = await category_repo.exists_codes(prediction.categories)
        categories = [c for c in prediction.categories if c in valid_codes]

        if not categories:
            if prediction.needs_clarification:
                clarification = await clarification_repo.create(
                    request_id=request.id,
                    question=prediction.question or "Уточните, пожалуйста, категорию обращения.",
                    step=1,
                )
                return CreateRequestResult(
                    request_id=request.id,
                    raw_text=request.raw_text,
                    is_toxic=is_toxic,
                    categories=[],
                    created_at=request.created_at,
                    clarification_needed=True,
                    clarification_question=clarification.question,
                )
            raise ValueError("Classifier returned no valid categories")

        await request_repo.replace_categories(
            request_id=request.id,
            categories=categories,
            confidence_map=prediction.confidence,
        )

        return CreateRequestResult(
            request_id=request.id,
            raw_text=request.raw_text,
            is_toxic=is_toxic,
            categories=[
                {"code": code, "confidence": prediction.confidence.get(code)}
                for code in categories
            ],
            created_at=request.created_at,
            clarification_needed=False
        )