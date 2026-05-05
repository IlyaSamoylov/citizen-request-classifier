from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def check_db(session: AsyncSession):
    await session.execute(text("SELECT 1"))

    result = await session.execute(text("SELECT COUNT(*) FROM categories"))
    count = result.scalar()

    return count