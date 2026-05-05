from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.models.clarification import Clarification
from app.models.request import Request
from app.models.request_category import RequestCategory


class AnalyticsRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def get_total_requests(self) -> int:
		result = await self.session.execute(select(func.count(Request.id)))
		return int(result.scalar_one() or 0)

	async def get_toxic_requests(self) -> int:
		result = await self.session.execute(select(func.count(Request.id)).where(Request.is_toxic.is_(True)))
		return int(result.scalar_one() or 0)

	async def get_clarification_requests(self) -> int:
		result = await self.session.execute(select(func.count(distinct(Clarification.request_id))))
		return int(result.scalar_one() or 0)

	async def get_category_stats(self) -> list[tuple[str, str, int]]:
		count_expr = func.count(RequestCategory.request_id)

		result = await self.session.execute(
			select(Category.code, Category.name, count_expr).select_from(Category)
			.outerjoin(RequestCategory, RequestCategory.category_code == Category.code)
			.group_by(Category.code, Category.name)
			.order_by(count_expr.desc(), Category.code.asc())
		)

		rows = result.all()
		return [(code, name, int(count or 0)) for code, name, count in rows]