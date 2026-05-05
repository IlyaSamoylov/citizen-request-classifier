from app.repos.category_repo import CategoryRepository
from app.repos.clarification_repo import ClarificationRepository
from app.repos.request_repo import RequestRepository
from app.services.classifier import ChatMessageDomain
from app.core.errors import RequestNotFoundError, ClassificationFailedError
from app.usecases.common import GetRequestResult, CreateRequestResult, to_request_result


class RequestUseCase:
    def __init__(self, request_repo: RequestRepository, category_repo: CategoryRepository,
                 clarification_repo: ClarificationRepository, classifier):
        self.request_repo = request_repo
        self.category_repo = category_repo
        self.clarification_repo = clarification_repo
        self.classifier = classifier

    async def create(self, text: str) -> CreateRequestResult:

        allowed_codes = await self.category_repo.get_all_codes()
        messages = [ChatMessageDomain(role="user", content=text)]
        prediction = await self.classifier.predict(messages=messages, allowed_codes=allowed_codes)
        is_toxic = prediction.is_toxic

        request = await self.request_repo.create(raw_text=text, is_toxic=is_toxic)
        valid_codes = set(await self.category_repo.exists_codes(prediction.categories))
        categories = [c for c in prediction.categories if c in valid_codes]

        if not categories:
            if prediction.needs_clarification:
                clarification = await self.clarification_repo.create(
                    request_id=request.id,
                    question=prediction.question or "Пожалуйста, уточните или переформулируйте запрос.",
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
            raise ClassificationFailedError(request.id)

        await self.request_repo.replace_categories(
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

    async def get_by_id(self, request_id: int) -> GetRequestResult:
        request = await self.request_repo.get_by_id(request_id)
        if not request:
            raise RequestNotFoundError(request_id)

        return to_request_result(request)