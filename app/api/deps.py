from fastapi import Request, Depends
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionLocal
from app.db.uow import UnitOfWork
from app.usecases.request import RequestUseCase
from app.usecases.clarification import ClarificationUseCase
from app.repos.request_repo import RequestRepository
from app.repos.category_repo import CategoryRepository
from app.repos.clarification_repo import ClarificationRepository


async def get_db() -> AsyncGenerator[AsyncSession, None]:
	async with SessionLocal() as session:
		yield session

async def get_uow(session: AsyncSession = Depends(get_db)) -> AsyncGenerator[UnitOfWork, None]:
	async with UnitOfWork(session) as uow:
		yield uow

def get_classifier(request: Request):
	return request.app.state.classifier

def get_toxicity_detector(request: Request):
	return request.app.state.toxicity_detector

def get_request_repo(uow: UnitOfWork = Depends(get_uow)) -> RequestRepository:
	return RequestRepository(uow.session)

def get_category_repo(uow: UnitOfWork = Depends(get_uow)) -> CategoryRepository:
	return CategoryRepository(uow.session)

def get_clarification_repo(uow: UnitOfWork = Depends(get_uow)) -> ClarificationRepository:
	return ClarificationRepository(uow.session)

def get_request_usecase(request_repo: RequestRepository = Depends(get_request_repo),
						category_repo: CategoryRepository = Depends(get_category_repo),
						clarification_repo: ClarificationRepository = Depends(get_clarification_repo),
                        classifier=Depends(get_classifier),
                        toxicity_detector=Depends(get_toxicity_detector)
						) -> RequestUseCase:
	return RequestUseCase(
        request_repo=request_repo, category_repo=category_repo, clarification_repo=clarification_repo,
        classifier=classifier, toxicity_detector=toxicity_detector
    )

def get_clarification_usecase(request_repo: RequestRepository = Depends(get_request_repo),
						category_repo: CategoryRepository = Depends(get_category_repo),
						clarification_repo: ClarificationRepository = Depends(get_clarification_repo),
                        classifier=Depends(get_classifier)
						) -> ClarificationUseCase:
	return ClarificationUseCase(
        request_repo=request_repo, category_repo=category_repo, clarification_repo=clarification_repo,
        classifier=classifier
    )