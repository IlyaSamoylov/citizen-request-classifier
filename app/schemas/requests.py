from pydantic import BaseModel, Field
from datetime import datetime

class RequestIn(BaseModel):
	text: str = Field(max_length=500)

class RequestOut(BaseModel):
	id: int

class RequestFull(BaseModel):
	id: int
	text: str
	labels: str
	confidence: float
	is_toxic: bool
	created_at: datetime

class ClarificationIn(BaseModel):
	answer: str