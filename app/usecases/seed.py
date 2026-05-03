from app.core.categories_loader import load_categories
from app.repos.category_repo import CategoryRepository
from app.core.errors import SeedCategoryException

async def seed_categories(repo: CategoryRepository) -> None:
    categories = load_categories()
    categories = deduplicate(categories)
    await repo.upsert_many(categories)

def deduplicate(items):
    seen = {}

    for item in items:
        if item.code in seen:
            raise SeedCategoryException(f"Повторяющаяся категория в справочнике: {item.code}")
        seen[item.code] = item

    return list(seen.values())