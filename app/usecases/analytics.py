from sqlalchemy.exc import SQLAlchemyError

from app.core.errors import PersistenceError
from app.repos.analytics_repo import AnalyticsRepository
from app.schemas.analytics import AnalyticsCategoryOut, AnalyticsOut


class AnalyticsUseCase:
	def __init__(self, analytics_repo: AnalyticsRepository):
		self.analytics_repo = analytics_repo

	async def get(self) -> AnalyticsOut:
		try:
			total_requests = await self.analytics_repo.get_total_requests()
			toxic_requests = await self.analytics_repo.get_toxic_requests()
			clarification_requests = await self.analytics_repo.get_clarification_requests()
			categories = await self.analytics_repo.get_category_stats()
		except SQLAlchemyError as exc:
			raise PersistenceError("Ошибка при получении аналитики") from exc

		toxic_share = round(toxic_requests / total_requests, 2) if total_requests else 0.0

		return AnalyticsOut(
			total_requests=total_requests,
			requests_by_cat=[
				AnalyticsCategoryOut(code=code, name=name,
				                     requests_count=requests_count)
				for code, name, requests_count in categories
			],
			toxic_rate=toxic_share,
			clarification_requests=clarification_requests,

		)