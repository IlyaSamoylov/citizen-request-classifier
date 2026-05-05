from pydantic import BaseModel, Field

class CategorySeed(BaseModel):
    code: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    synonyms: list[str] = Field(min_length=1)
    examples: list[str] = Field(min_length=1)