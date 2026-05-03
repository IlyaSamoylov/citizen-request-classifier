import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.schemas.category_seed import CategorySeed


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_many(self, items: list[CategorySeed]) -> None:
        result = await self.session.execute(select(Category))
        existing = {obj.code: obj for obj in result.scalars()}

        for item in items:
            obj = existing.get(item.code)
            if obj:
                obj.name = item.name
                obj.description = item.description
                obj.synonyms = json.dumps(item.synonyms, ensure_ascii=False)
                obj.examples = json.dumps(item.examples, ensure_ascii=False)
            else:
                self.session.add(
                    Category(
                        code=item.code,
                        name=item.name,
                        description=item.description,
                        synonyms=json.dumps(item.synonyms, ensure_ascii=False),
                        examples=json.dumps(item.examples, ensure_ascii=False),
                    )
                )

        await self.session.flush()

    async def exists_codes(self, codes: list[str]) -> set[str]:
        result = await self.session.execute(
            select(Category.code).where(Category.code.in_(codes))
        )
        return set(result.scalars())