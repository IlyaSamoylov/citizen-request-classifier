from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.clarification import Clarification


class ClarificationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, request_id: int, question: str, step: int) -> Clarification:
        obj = Clarification(request_id=request_id, question=question, step=step)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def add_answer(self, clarification_id: int, answer: str):
        result = await self.session.execute(select(Clarification).where(Clarification.id == clarification_id))
        obj = result.scalar_one_or_none()
        if obj is None:
            return
        obj.answer = answer

    async def get_last_by_request_id(self, request_id: int) -> Clarification | None:
        result = await self.session.execute(
            select(Clarification)
            .where(Clarification.request_id == request_id)
            .order_by(Clarification.step.desc(), Clarification.id.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_last_step(self, request_id: int) -> int:
        result = await self.session.execute(
            select(Clarification.step)
            .where(Clarification.request_id == request_id)
            .order_by(Clarification.step.desc())
            .limit(1)
        )
        last = result.scalar_one_or_none()
        return last or 0