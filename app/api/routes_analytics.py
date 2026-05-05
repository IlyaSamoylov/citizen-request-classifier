from fastapi import APIRouter, Depends

from app.api.deps import get_analytics_usecase
from app.schemas.analytics import AnalyticsOut
from app.usecases.analytics import AnalyticsUseCase

analytics_router = APIRouter(prefix="/analytics", tags=["analytics"])

@analytics_router.get("", response_model=AnalyticsOut)
async def get_analytics(usecase: AnalyticsUseCase = Depends(get_analytics_usecase)):
	return await usecase.get()
