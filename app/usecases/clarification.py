from sqlalchemy.exc import SQLAlchemyError

from app.repos.category_repo import CategoryRepository
from app.repos.clarification_repo import ClarificationRepository
from app.repos.request_repo import RequestRepository
from app.core.errors import (
    ClarificationAlreadyAnsweredError,
    ClarificationNotFoundError,
    ClassificationFailedError,
    PersistenceError,
    RequestNotFoundError,
)
from app.usecases.common import GetRequestResult, to_request_result

class ClarificationUseCase:
    def __init__(self, request_repo: RequestRepository, clarification_repo: ClarificationRepository,
        category_repo: CategoryRepository, classifier):
        self.request_repo = request_repo
        self.clarification_repo = clarification_repo
        self.category_repo = category_repo
        self.classifier = classifier

    async def _apply_prediction(self, request_id: int, clarification_step: int, prediction) -> None:
        valid_codes = await self.category_repo.exists_codes(prediction.categories)
        categories = [code for code in prediction.categories if code in valid_codes]

        if categories:
            await self.request_repo.replace_categories(
                request_id=request_id,
                categories=categories,
                confidence_map=prediction.confidence,
            )
            return

        if prediction.needs_clarification:
            await self.clarification_repo.create(
                request_id=request_id,
                question=prediction.question or "Уточните, пожалуйста, категорию обращения.",
                step=clarification_step + 1,
            )
            return

        raise ClassificationFailedError(request_id)

    async def _get_request_or_raise(self, request_id: int):
        request = await self.request_repo.get_by_id(request_id)
        if request is None:
            raise RequestNotFoundError(request_id)

        return request

    async def answer(self, request_id: int, answer: str) -> GetRequestResult:
        try:
            request = await self._get_request_or_raise(request_id)

            clarification = await self.clarification_repo.get_last_by_request_id(request_id)
            if clarification is None:
                raise ClarificationNotFoundError(request_id)

            if clarification.answer is not None:
                raise ClarificationAlreadyAnsweredError(clarification.id)

            await self.clarification_repo.add_answer(clarification.id, answer)

            text_for_classifier = f"{request.raw_text}\n{answer}"
            prediction = await self.classifier.predict(text_for_classifier)

            await self._apply_prediction(request_id=request_id, clarification_step=clarification.step,
                                         prediction=prediction)

            await self.request_repo.mark_updated(request_id)

            request = await self._get_request_or_raise(request_id)
            return to_request_result(request)

        except SQLAlchemyError as exc:
            raise PersistenceError("Ошибка при сохранении ответа") from exc



