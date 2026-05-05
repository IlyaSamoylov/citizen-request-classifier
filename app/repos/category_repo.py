import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.schemas.category_seed import CategorySeed

class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_many(self, items: list[CategorySeed]):
        items_by_code = {item.code: item for item in items}
        new_codes = set(items_by_code)

        result = await self.session.execute(select(Category).where(Category.code.in_(new_codes)))
        existing = {obj.code: obj for obj in result.scalars()}

        for code, item in items_by_code.items():

            obj = existing.get(code)
            if obj:
                obj.name = item.name
                obj.description = item.description
                obj.synonyms = json.dumps(item.synonyms, ensure_ascii=False)
                obj.examples = json.dumps(item.examples, ensure_ascii=False)
            else:
                self.session.add(
                    Category(
                        code=item.code, name=item.name,
                        description=item.description,
                        synonyms=json.dumps(item.synonyms, ensure_ascii=False),
                        examples=json.dumps(item.examples, ensure_ascii=False),
                    )
                )

        await self.session.flush()

    async def get_all_codes(self) -> list[str]:
        result = await self.session.execute(select(Category.code).order_by(Category.code.asc()))
        return list(result.scalars())

    async def exists_codes(self, codes: list[str]) -> set[str]:
        result = await self.session.execute(select(Category.code).where(Category.code.in_(codes)))
        return set(result.scalars())