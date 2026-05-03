from fastapi import APIRouter, Depends

from app.schemas.requests import RequestIn, RequestOut, RequestFull, RequestCategoryOut
from app.usecases.request import RequestUseCase
from app.schemas.clarification import ClarificationAnswerIn
from app.usecases.clarification import ClarificationUseCase
from app.api.deps import get_request_usecase, get_clarification_usecase

requests_router = APIRouter(prefix="/requests", tags=["requests"])

@requests_router.post("", response_model=RequestOut)
async def post_request(request: RequestIn, usecase: RequestUseCase = Depends(get_request_usecase)):
	result = await usecase.create(request.text)

	return RequestOut(id=result.request_id, raw_text=request.text,
	                  categories=[RequestCategoryOut(**item) for item in result.categories],
	                  is_toxic=result.is_toxic, clarification_question=result.clarification_question,
	                  created_at=result.created_at)


@requests_router.get("/{id}", response_model=RequestFull)
async def get_request(request_id: int, usecase: RequestUseCase = Depends(get_request_usecase)):
	result = await usecase.get_by_id(request_id)

	return RequestFull(
		id=result.request_id,
		raw_text=result.raw_text,
		categories=[RequestCategoryOut(**item) for item in result.categories],
		is_toxic=result.is_toxic,
		clarifications=result.clarifications,
		created_at=result.created_at,
		updated_at=result.updated_at,
	)

@requests_router.post("/{id}/clarifications")
async def post_clarifications(request_id: int, answer: ClarificationAnswerIn, usecase: ClarificationUseCase = Depends(get_clarification_usecase)):

	result = await usecase.answer(request_id=request_id, answer=answer.answer)

	return RequestFull(
		id=result.request_id,
		raw_text=result.raw_text,
		categories=result.categories,
		is_toxic=result.is_toxic,
		clarifications=result.clarifications,
		created_at=result.created_at,
		updated_at=result.updated_at,
	)

