from fastapi import APIRouter

from app.schemas.analytics import AnalyticsOut

analytics_router = APIRouter(prefix="/analytics", tags=["analytics"])

@analytics_router.get("", response_model=AnalyticsOut)
async def get_analytics():
	pass
