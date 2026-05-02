from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category


async def check_db(session: AsyncSession):
    # 1. Проверка соединения
    await session.execute(text("SELECT 1"))

    # 2. Проверка, что категории есть
    result = await session.execute(select(Category))
    categories = result.scalars().all()

    if not categories:
        raise RuntimeError("Categories table is empty")

    return len(categories)