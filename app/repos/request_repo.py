from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone

from app.models.request import Request
from app.models.request_category import RequestCategory


class RequestRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, raw_text: str, is_toxic: bool) -> Request:
        obj = Request(raw_text=raw_text, is_toxic=is_toxic)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def replace_categories(
        self,
        request_id: int,
        categories: list[str],
        confidence_map: dict[str, float] | None = None,
    ) -> None:
        await self.session.execute(
            delete(RequestCategory).where(RequestCategory.request_id == request_id)
        )

        objs = []
        for code in categories:
            objs.append(
                RequestCategory(
                    request_id=request_id,
                    category_code=code,
                    confidence=None if not confidence_map else confidence_map.get(code),
                )
            )

        self.session.add_all(objs)

    async def get_by_id(self, request_id: int) -> Request | None:
        result = await self.session.execute(
            select(Request)
            .where(Request.id == request_id)
            .options(
                selectinload(Request.request_categories).selectinload(RequestCategory.category),
                selectinload(Request.clarifications),
            )
        )
        return result.scalar_one_or_none()

    async def mark_updated(self, request_id: int) -> None:
        await self.session.execute(
            update(Request)
            .where(Request.id == request_id)
            .values(updated_at=datetime.now(timezone.utc))
        )