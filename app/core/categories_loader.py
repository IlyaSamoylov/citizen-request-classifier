import yaml
from pathlib import Path

from app.core.config import settings
from app.schemas.category_seed import CategorySeed

def load_categories() -> list[CategorySeed]:
    path = Path(settings.CATEGORIES_FILE)

    if not path.exists():
        raise FileNotFoundError(f"Справочник категорий не найден: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data:
        raise ValueError(f"Справочник пуст")

    return [CategorySeed(**item) for item in data]