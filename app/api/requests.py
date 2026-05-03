from fastapi import APIRouter, Depends

from app.schemas.requests import RequestIn, RequestOut, RequestFull, RequestCategoryOut
from app.db.uow import UnitOfWork
from app.db.session import get_uow
from app.usecases.request import RequestUseCase
from app.services.classifier import DummyClassifier
from app.services.toxicity import DummyToxicityDetector

requests_router = APIRouter(prefix="/requests", tags=["requests"])

@requests_router.post("", response_model=RequestOut)
async def post_request(request: RequestIn, uow: UnitOfWork = Depends(get_uow)):
	usecase = RequestUseCase(classifier=DummyClassifier(), toxicity_detector=DummyToxicityDetector())
	result = await usecase.create(uow, request.text)

	return RequestOut(id=result.request_id, raw_text=request.text,
	                  categories=[RequestCategoryOut(**item) for item in result.categories],
	                  is_toxic=result.is_toxic, clarification_question=result.clarification_question,
	                  created_at=result.created_at)


@requests_router.get("/{id}", response_model=RequestFull)
async def get_request(id: int):
	pass

@requests_router.post("/{id}/clarifications")
async def post_clarifications(id: int):
	pass

