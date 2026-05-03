from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.session import SessionLocal
from app.usecases.seed import seed_categories
from app.api.analytics import analytics_router
from app.api.requests import requests_router
from app.core.config import settings
from app.repos.category_repo import CategoryRepository
from app.api.exc_handlers import app_error_handler
from app.services.classifier import DummyClassifier
from app.services.toxicity import DummyToxicityDetector
from app.core.errors import BaseAppException

from app.db.healthcheck import check_db

@asynccontextmanager
async def lifespan(app: FastAPI):
	"""Cоздание таблицы из справочника категорий до запуска"""
	async with SessionLocal() as session:
		async with session.begin():
			repo = CategoryRepository(session)
			await seed_categories(repo)

		count = await check_db(session)
		print(f"[OK] DB connected, categories loaded: {count}")

	app.state.classifier = DummyClassifier()
	app.state.toxicity_detector = DummyToxicityDetector()

	yield


def create_app() -> FastAPI:
	"""Функция для создания FastAPI приложения"""
	app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
	app.include_router(requests_router)
	app.include_router(analytics_router)
	app.add_exception_handler(BaseAppException, app_error_handler)

	@app.get("/health")
	async def health():
		"""Проверка состояния приложения"""
		return {"status": "ok", "env": settings.APP_ENV}

	return app

app = create_app()