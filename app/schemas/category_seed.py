from pydantic import BaseModel

class CategorySeed(BaseModel):
    code: str
    name: str