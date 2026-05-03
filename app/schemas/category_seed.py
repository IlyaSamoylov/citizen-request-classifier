from pydantic import BaseModel

class CategorySeed(BaseModel):
    code: str
    name: str
    description: str
    synonyms: list[str]
    examples: list[str]