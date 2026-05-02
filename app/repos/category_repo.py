from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.category import Category
from app.schemas.category_seed import CategorySeed

class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_many(self, items: list[CategorySeed]) -> None:
        result = await self.session.execute(select(Category))
        existing = {cat.code: cat for cat in result.scalars()}

        for item in items:
            obj = existing.get(item.code)

            if obj:
                if obj.name != item.name:
                    obj.name = item.name
            else:
                self.session.add(Category(code=item.code, name=item.name))

        await self.session.commit()